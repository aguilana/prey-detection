import cv2
import signal
import sys
import os
from datetime import datetime

def signal_handler(sig, frame):
    print("\nInterrupted! Saving video...")
    if 'cap' in globals() and cap.isOpened():
        cap.release()
    if 'out' in globals():
        out.release()
        print(f"Video saved as {output_file} with {frame_count} frames.")
    if cv2.getWindowProperty("Recording - Press q to stop", cv2.WND_PROP_VISIBLE) >= 1:
        cv2.destroyAllWindows()
    sys.exit(0)

# Register the signal handler for Ctrl+C and Ctrl+X
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set up video writer
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"videos/cat/chatty_video_{timestamp}.mp4"
# Use MP4V codec instead of XVID for better compatibility
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))

# Ensure we've captured at least some frames
frame_count = 0
min_frames = 30  # At least 1.5 seconds at 20fps

print(f"Recording video to {output_file}. Press 'q' to stop recording.")
try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Write the frame to the video file
        out.write(frame)
        frame_count += 1
        
        # Display the frame with frame count
        cv2.putText(frame, f"Frames: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Recording - Press q to stop", frame)
        
        # Handle multiple exit keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:  # q or ESC key
            print("Quitting...")
            break
        
except Exception as e:
    print(f"Error during recording: {e}")
finally:
    # Always release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    if frame_count < min_frames:
        print(f"Warning: Only captured {frame_count} frames, video may be too short.")
    else:
        print(f"Video saved as {output_file} with {frame_count} frames.")
