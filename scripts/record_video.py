#!/usr/bin/env python3
"""
Video recording script for cat videos.
"""
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prey_detection.capture.camera import Camera
from prey_detection.capture.recorder import VideoRecorder
from prey_detection.config.settings import PATHS

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Record video")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--duration", type=int, help="Record for specified duration (seconds)")
    parser.add_argument("--mode", choices=["interactive", "duration"], default="interactive",
                       help="Recording mode")
    args = parser.parse_args()
    
    # Determine output directory
    output_dir = args.output_dir or PATHS["cat_videos_dir"]
    
    # Setup camera and recorder
    camera = Camera(camera_index=args.camera)
    recorder = VideoRecorder(output_dir=output_dir, camera=camera)
    
    try:
        if args.mode == "duration" or args.duration:
            if not args.duration:
                print("Error: Duration must be specified for duration mode")
                return 1
            
            print(f"Recording for {args.duration} seconds...")
            recorder.record_duration(args.duration)
        else:
            print("Starting interactive recording mode...")
            recorder.record_interactive()
    except KeyboardInterrupt:
        print("\nRecording stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())