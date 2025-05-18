#!/usr/bin/env python3
"""
Extract frames from videos for model training.
"""
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prey_detection.processing.frames import FrameExtractor
from prey_detection.config.settings import PATHS

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--interval", type=int, default=1, 
                       help="Extract every Nth frame (default: 1)")
    parser.add_argument("--start-time", type=float, help="Start time in seconds")
    parser.add_argument("--end-time", type=float, help="End time in seconds")
    parser.add_argument("--start-frame", type=int, help="Start frame number")
    parser.add_argument("--end-frame", type=int, help="End frame number")
    parser.add_argument("--max-frames", type=int, help="Maximum number of frames to extract")
    args = parser.parse_args()
    
    # Determine output directory
    output_dir = args.output_dir
    
    # Setup frame extractor
    extractor = FrameExtractor()
    
    try:
        if args.start_frame is not None and args.end_frame is not None:
            # Extract frame range
            extractor.extract_frames_range(
                args.video_path,
                args.start_frame,
                args.end_frame,
                output_dir
            )
        else:
            # Extract by interval
            extractor.extract_frames(
                args.video_path,
                output_dir,
                args.interval,
                args.start_time,
                args.end_time,
                args.max_frames
            )
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())