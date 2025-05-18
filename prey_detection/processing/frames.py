"""Frame extraction and processing utilities."""
import cv2
import os
import numpy as np
from pathlib import Path
from datetime import datetime
from ..config.settings import PATHS

class FrameExtractor:
    """Extract frames from videos for analysis and model training."""
    
    def __init__(self, output_dir=None):
        """Initialize the frame extractor.
        
        Args:
            output_dir (str): Base directory to save extracted frames
        """
        self.output_dir = output_dir or PATHS["frames_dir"]
        os.makedirs(self.output_dir, exist_ok=True)
        
    def extract_frames(self, video_path, output_dir=None, frame_interval=1, 
                      start_time=None, end_time=None, max_frames=None):
        """Extract frames from a video file.
        
        Args:
            video_path (str): Path to the video file
            output_dir (str): Directory to save frames (if None, uses video filename)
            frame_interval (int): Extract every Nth frame
            start_time (float): Start time in seconds
            end_time (float): End time in seconds
            max_frames (int): Maximum number of frames to extract
            
        Returns:
            tuple: (num_frames, output_dir) - Number of frames extracted and output dir
        """
        # Verify video exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Create output directory
        if output_dir is None:
            video_name = Path(video_path).stem
            output_dir = os.path.join(self.output_dir, f"{video_name}_frames")
            
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
            
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Convert times to frame numbers
        start_frame = 0
        if start_time is not None:
            start_frame = int(start_time * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
        end_frame = total_frames
        if end_time is not None:
            end_frame = min(int(end_time * fps), total_frames)
            
        print(f"Video: {video_path}")
        print(f"Total frames: {total_frames}")
        print(f"FPS: {fps}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Extracting frames {start_frame} to {end_frame}")
        print(f"Frame interval: {frame_interval}")
        
        # Extract frames
        frame_count = 0
        saved_count = 0
        
        while frame_count < end_frame:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Extract frame if it's on the interval
            if (frame_count - start_frame) % frame_interval == 0:
                # Save frame
                frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_count += 1
                
                # Print progress
                if saved_count % 10 == 0:
                    print(f"Saved {saved_count} frames...")
                    
                # Check if we've reached max frames
                if max_frames is not None and saved_count >= max_frames:
                    break
                    
            frame_count += 1
            
        # Release resources
        cap.release()
        
        print(f"Extraction complete: {saved_count} frames saved to {output_dir}")
        return saved_count, output_dir
        
    def extract_frames_range(self, video_path, start_frame, end_frame, output_dir=None):
        """Extract a specific range of frames from a video.
        
        Args:
            video_path (str): Path to video file
            start_frame (int): Start frame number
            end_frame (int): End frame number
            output_dir (str): Directory to save frames
            
        Returns:
            tuple: (num_frames, output_dir)
        """
        # Verify video exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Create output directory
        if output_dir is None:
            video_name = Path(video_path).stem
            range_str = f"{start_frame}-{end_frame}"
            output_dir = os.path.join(self.output_dir, f"{video_name}_{range_str}")
            
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
            
        # Set position to start frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Extract frames
        frame_count = start_frame
        saved_count = 0
        
        while frame_count <= end_frame:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Save frame
            frame_filename = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            # Print progress
            if saved_count % 10 == 0:
                print(f"Saved {saved_count} frames...")
                
            frame_count += 1
            
        # Release resources
        cap.release()
        
        print(f"Extraction complete: {saved_count} frames saved to {output_dir}")
        return saved_count, output_dir
        
    @staticmethod
    def create_test_frames(output_dir, num_frames=10, width=640, height=480):
        """Create test frames with various patterns and shapes.
        
        Args:
            output_dir (str): Directory to save test frames
            num_frames (int): Number of frames to create
            width (int): Frame width
            height (int): Frame height
            
        Returns:
            str: Path to the output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(num_frames):
            # Create a blank frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Draw some shapes
            # Circle moving across
            circle_x = int(width * (i / num_frames))
            cv2.circle(frame, (circle_x, height // 3), 50, (0, 0, 255), -1)
            
            # Rectangle moving up and down
            rect_y = int(height * 0.5 * (1 + np.sin(i * np.pi / (num_frames/2))))
            cv2.rectangle(frame, (width//2 - 60, rect_y - 30), 
                         (width//2 + 60, rect_y + 30), (0, 255, 0), -1)
            
            # Text
            cv2.putText(frame, f"Test Frame {i+1}/{num_frames}", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Save the frame
            frame_filename = os.path.join(output_dir, f"test_frame_{i:03d}.jpg")
            cv2.imwrite(frame_filename, frame)
            
        print(f"Created {num_frames} test frames in {output_dir}")
        return output_dir