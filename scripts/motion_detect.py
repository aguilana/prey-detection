#!/usr/bin/env python3
"""
Motion detection script for automatic recording when motion is detected.
"""
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prey_detection.capture.camera import Camera
from prey_detection.capture.motion import MotionDetector
from prey_detection.config.settings import PATHS, MOTION_SETTINGS

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Motion detection and recording")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--threshold", type=int, 
                       help=f"Motion threshold (default: {MOTION_SETTINGS['frame_diff_threshold']})")
    parser.add_argument("--duration", type=int, 
                       help=f"Recording duration in seconds (default: {MOTION_SETTINGS['record_seconds']})")
    parser.add_argument("--interval", type=float, 
                       help=f"Motion check interval in seconds (default: {MOTION_SETTINGS['motion_check_interval']})")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview window")
    args = parser.parse_args()
    
    # Determine output directory
    output_dir = args.output_dir or PATHS["motion_videos_dir"]
    
    # Setup camera and detector
    camera = Camera(camera_index=args.camera)
    detector = MotionDetector(output_dir=output_dir, camera=camera)
    
    # Override settings if provided
    if args.threshold is not None:
        detector.frame_diff_threshold = args.threshold
        
    if args.duration is not None:
        detector.record_seconds = args.duration
        
    if args.interval is not None:
        detector.motion_check_interval = args.interval
    
    try:
        detector.start_monitoring(show_preview=not args.no_preview)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())