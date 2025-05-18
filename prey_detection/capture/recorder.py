"""Video recording functionality."""
import cv2
import os
import time
import signal
import sys
from datetime import datetime
from ..config.settings import VIDEO_SETTINGS, PATHS
from .camera import Camera

class VideoRecorder:
    """Video recorder class for recording video from a camera."""
    
    def __init__(self, output_dir=None, camera=None, resolution=None):
        """Initialize the recorder.
        
        Args:
            output_dir (str): Directory to save videos
            camera (Camera): Camera instance to use
            resolution (tuple): Resolution (width, height)
        """
        self.output_dir = output_dir or PATHS["cat_videos_dir"]
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.camera = camera or Camera()
        if not isinstance(self.camera, Camera):
            raise TypeError("camera must be an instance of Camera")
            
        self.resolution = resolution or VIDEO_SETTINGS["resolution"]
        self.fps = VIDEO_SETTINGS["fps"]
        self.codec = VIDEO_SETTINGS["codec"]
        self.extension = VIDEO_SETTINGS["extension"]
        
        self.output_file = None
        self.writer = None
        self.recording = False
        self.frame_count = 0
        
    def __enter__(self):
        """Context manager entry."""
        if not self.camera.cap:
            self.camera.open()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        
    def start(self, output_file=None):
        """Start recording.
        
        Args:
            output_file (str): Path to save the video
            
        Returns:
            str: Path to the output file
        """
        if self.recording:
            raise RuntimeError("Already recording")
            
        if not output_file:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_file = os.path.join(self.output_dir, f"video_{timestamp}{self.extension}")
            
        self.output_file = output_file
        
        # Create the video writer
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self.writer = cv2.VideoWriter(
            self.output_file, 
            fourcc, 
            self.fps, 
            self.resolution
        )
        
        self.recording = True
        self.frame_count = 0
        
        return self.output_file
        
    def write_frame(self, frame):
        """Write a frame to the video.
        
        Args:
            frame: The frame to write
            
        Returns:
            int: Current frame count
        """
        if not self.recording:
            raise RuntimeError("Not recording")
            
        # Resize if necessary
        if frame.shape[1] != self.resolution[0] or frame.shape[0] != self.resolution[1]:
            frame = cv2.resize(frame, self.resolution)
            
        self.writer.write(frame)
        self.frame_count += 1
        
        return self.frame_count
        
    def stop(self):
        """Stop recording.
        
        Returns:
            tuple: (output_file, frame_count)
        """
        if not self.recording:
            return None, 0
            
        self.recording = False
        if self.writer:
            self.writer.release()
            self.writer = None
            
        return self.output_file, self.frame_count
        
    def record_duration(self, duration, show_preview=True):
        """Record for a specific duration.
        
        Args:
            duration (float): Duration in seconds
            show_preview (bool): Show preview window
            
        Returns:
            tuple: (output_file, frame_count)
        """
        if not self.camera.cap or not self.camera.cap.isOpened():
            self.camera.open()
            
        self.start()
        
        start_time = time.time()
        preview_name = "Recording" if show_preview else None
        
        while time.time() - start_time < duration:
            frame = self.camera.read()
            
            # Add recording indicator
            cv2.putText(
                frame, 
                f"REC {self.frame_count} | {int(time.time() - start_time)}s", 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (0, 0, 255), 
                2
            )
            
            self.write_frame(frame)
            
            if show_preview:
                cv2.imshow(preview_name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        if show_preview:
            cv2.destroyWindow(preview_name)
            
        return self.stop()
        
    def record_interactive(self, window_name="Video Recorder"):
        """Record interactively with user interface.
        
        Args:
            window_name (str): Name of the preview window
            
        Returns:
            tuple: (output_file, frame_count)
        """
        if not self.camera.cap or not self.camera.cap.isOpened():
            self.camera.open()
            
        recording = False
        output_file = None
        frame_count = 0
        
        def process_frame(frame):
            nonlocal recording
            
            # Add UI indicators
            if recording:
                # Add recording indicator 
                cv2.putText(
                    frame, 
                    f"REC • Frames: {self.frame_count}", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (0, 0, 255), 
                    2
                )
                # Red circle
                cv2.circle(frame, (20, 60), 8, (0, 0, 255), -1)
                
                # Write frame
                self.write_frame(frame)
            else:
                # Ready indicator
                cv2.putText(
                    frame, 
                    "Ready - Press 'r' to record", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (0, 255, 0), 
                    2
                )
                
            # Instructions
            cv2.putText(
                frame, 
                "r: record/stop | q: quit | space: screenshot", 
                (10, frame.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (255, 255, 255), 
                1
            )
            
            return frame
            
        def key_handler(key):
            nonlocal recording, output_file, frame_count
            
            if key == ord('r'):
                if recording:
                    # Stop recording
                    output_file, frame_count = self.stop()
                    recording = False
                    print(f"Recording stopped. Saved {frame_count} frames to {output_file}")
                else:
                    # Start recording
                    output_file = self.start()
                    recording = True
                    print(f"Recording started: {output_file}")
            elif key == ord(' '):
                # Take screenshot
                screenshot_dir = os.path.join(self.output_dir, "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.jpg")
                cv2.imwrite(screenshot_path, self.camera.read())
                print(f"Screenshot saved: {screenshot_path}")
            elif key == ord('q'):
                if recording:
                    output_file, frame_count = self.stop()
                    print(f"Recording stopped. Saved {frame_count} frames to {output_file}")
                return False  # Stop the camera loop
                
            return True
            
        def display(frame):
            processed_frame = process_frame(frame)
            cv2.imshow(window_name, processed_frame)
            key = cv2.waitKey(1) & 0xFF
            return key_handler(key)
            
        try:
            print(f"Camera: {self.camera.camera_index}")
            print(f"Resolution: {self.resolution[0]}x{self.resolution[1]}")
            print(f"FPS: {self.fps}")
            print("\nCommands:")
            print("  R - Start/Stop Recording")
            print("  Q - Quit")
            print("  Space - Take Screenshot")
            
            # Read frames continuously 
            self.camera.read_continuous(callback=display)
        finally:
            if recording:
                output_file, frame_count = self.stop()
                
        return output_file, frame_count