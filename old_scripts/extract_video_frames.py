import cv2
import os
import argparse
from datetime import datetime

def extract_frames(input_video, output_dir, frame_interval=1):
    """
    Extract frames from a video file at specified intervals.
    
    Args:
        input_video (str): Path to input video file
        output_dir (str): Directory to save extracted frames
        frame_interval (int): Save every nth frame
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Open video file
    cap = cv2.VideoCapture(input_video)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video}")
        return False
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video: {input_video}")
    print(f"Total frames: {total_frames}")
    print(f"FPS: {fps}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Extracting every {frame_interval} frame(s)")
    
    # Extract frames
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Save frame at specified interval
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            # Print progress periodically
            if saved_count % 10 == 0:
                print(f"Saved {saved_count} frames...")
        
        frame_count += 1
    
    # Release resources
    cap.release()
    
    print(f"\nExtraction complete: {saved_count} frames saved to {output_dir}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video file")
    parser.add_argument("input_video", help="Path to input video file")
    parser.add_argument("--output-dir", help="Directory to save extracted frames")
    parser.add_argument("--interval", type=int, default=1, help="Save every nth frame (default: 1)")
    
    args = parser.parse_args()
    
    # If output directory not specified, create one based on video filename
    if not args.output_dir:
        video_name = os.path.splitext(os.path.basename(args.input_video))[0]
        args.output_dir = os.path.join("frames", video_name + "_frames")
    
    # Extract frames
    extract_frames(args.input_video, args.output_dir, args.interval)