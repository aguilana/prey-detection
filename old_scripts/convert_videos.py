import cv2
import os
import glob
from datetime import datetime

def convert_avi_to_mp4(input_path, output_path):
    """Convert AVI to MP4 with mp4v codec for better compatibility."""
    print(f"Converting {input_path} to {output_path}")
    
    # Open the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return False
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 20.0  # Default to 20fps if unable to detect
    
    # Create VideoWriter with mp4v codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    # Process frames
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        out.write(frame)
        frame_count += 1
        
        # Show progress every 50 frames
        if frame_count % 50 == 0:
            print(f"Processed {frame_count} frames...")
    
    # Release resources
    cap.release()
    out.release()
    
    if frame_count > 0:
        print(f"✅ Successfully converted to {output_path} with {frame_count} frames")
        return True
    else:
        print(f"❌ Failed to extract any frames from {input_path}")
        return False

def convert_all_videos(source_dirs, target_dir):
    """Convert all AVI videos in the source directories to MP4 format."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    total_videos = 0
    successful_conversions = 0
    
    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
            print(f"Warning: Source directory {source_dir} does not exist. Skipping.")
            continue
            
        # Get all AVI files in the source directory
        avi_files = glob.glob(os.path.join(source_dir, "*.avi"))
        
        for avi_file in avi_files:
            total_videos += 1
            file_name = os.path.basename(avi_file)
            output_name = os.path.splitext(file_name)[0] + ".mp4"
            output_path = os.path.join(target_dir, output_name)
            
            if convert_avi_to_mp4(avi_file, output_path):
                successful_conversions += 1
                
    print(f"\nConversion complete: {successful_conversions}/{total_videos} videos successfully converted")
    return successful_conversions

if __name__ == "__main__":
    # Convert videos from all directories
    source_directories = [
        "videos/cat",
        "videos/human",
        "videos/motion"
    ]
    target_directory = "videos/converted"
    
    print(f"Starting video conversion at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    convert_all_videos(source_directories, target_directory)
    print(f"Conversion finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nConverted videos are in: {os.path.abspath(target_directory)}")