import cv2
import os
import signal
import sys
from datetime import datetime

# Initialize global frame counter
frame_count = 0
recording = False
output_file = ""

def signal_handler(sig, frame):
    """Handle graceful shutdown on Ctrl+C."""
    print("\n\nSaving video and exiting...")
    if 'cap' in globals() and cap.isOpened():
        cap.release()
    if 'out' in globals() and recording:
        out.release()
        print(f"Video saved with {frame_count} frames: {output_file}")
    cv2.destroyAllWindows()
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Ensure output directory exists
output_dir = "videos/cat"
os.makedirs(output_dir, exist_ok=True)

# Initialize camera
camera_index = 0  # Default camera
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print(f"Error: Could not open camera {camera_index}.")
    sys.exit(1)

# Get camera properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 20.0

# Print camera info
print(f"Camera: {camera_index}")
print(f"Resolution: {frame_width}x{frame_height}")
print(f"FPS: {fps}")
print("\nCommands:")
print("  R - Start/Stop Recording")
print("  Q - Quit")
print("  Space - Take Screenshot")

# Main loop
try:
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
            
        # Add frame counter if recording
        if recording:
            cv2.putText(frame, f"REC • Frames: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Add red dot indicator
            cv2.circle(frame, (20, 60), 8, (0, 0, 255), -1)
            
            # Write frame to video
            out.write(frame)
            frame_count += 1
        else:
            cv2.putText(frame, "Ready - Press 'r' to record", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        # Display the frame
        cv2.imshow("Cat Video Recorder", frame)
        
        # Process key presses
        key = cv2.waitKey(1) & 0xFF
        
        # Handle key presses
        if key == ord('q'):
            print("Quitting...")
            break
        elif key == ord('r'):
            if recording:
                # Stop recording
                out.release()
                print(f"Recording stopped. Saved {frame_count} frames to {output_file}")
                recording = False
            else:
                # Start recording
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_file = os.path.join(output_dir, f"cat_video_{timestamp}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
                frame_count = 0
                recording = True
                print(f"Recording started: {output_file}")
        elif key == 32:  # Spacebar
            # Take screenshot
            screenshot_dir = os.path.join(output_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.jpg")
            cv2.imwrite(screenshot_path, frame)
            print(f"Screenshot saved: {screenshot_path}")
            
except Exception as e:
    print(f"Error: {e}")
finally:
    # Release resources
    if cap.isOpened():
        cap.release()
    if 'out' in locals() and recording:
        out.release()
    cv2.destroyAllWindows()
    
    if recording and frame_count > 0:
        print(f"Video saved with {frame_count} frames: {output_file}")