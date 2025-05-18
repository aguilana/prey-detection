import cv2
import numpy as np
import os
import time

def create_test_video(output_path, duration=5, fps=20, width=640, height=480):
    """Creates a test video with moving shapes to verify video player works."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frames = int(duration * fps)
    for i in range(frames):
        # Create a black frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add timestamp
        cv2.putText(frame, f"Frame: {i+1}/{frames}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add moving circle
        x = int(width/2 + width/4 * np.sin(i/10))
        y = int(height/2 + height/4 * np.cos(i/10))
        cv2.circle(frame, (x, y), 30, (0, 0, 255), -1)
        
        # Add moving rectangle
        x2 = int(width/2 + width/4 * np.cos(i/15))
        y2 = int(height/2 + height/4 * np.sin(i/15))
        cv2.rectangle(frame, (x2-30, y2-30), (x2+30, y2+30), (0, 255, 0), -1)
        
        # Write frame to video
        out.write(frame)
    
    out.release()
    print(f"Test video created at {output_path}")
    print(f"Video specs: {frames} frames, {fps} fps, {duration} seconds")

if __name__ == "__main__":
    test_video_path = "videos/cat/fixed/test_video.mp4"
    create_test_video(test_video_path)
    
    print("\nYou should now be able to open this test video in VLC player.")
    print("If you can open this video but not your recorded videos, the issue is with the recording process.")