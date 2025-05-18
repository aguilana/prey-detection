"""Motion detection and recording."""
import cv2
import os
import time
from datetime import datetime
from ..config.settings import MOTION_SETTINGS, PATHS
from .camera import Camera
from .recorder import VideoRecorder

class MotionDetector:
    """Motion detection class for motion-triggered recording."""
    
    def __init__(self, output_dir=None, camera=None):
        """Initialize the motion detector.
        
        Args:
            output_dir (str): Directory to save motion videos
            camera (Camera): Camera instance to use
        """
        self.output_dir = output_dir or PATHS["motion_videos_dir"]
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.camera = camera or Camera()
        if not isinstance(self.camera, Camera):
            raise TypeError("camera must be an instance of Camera")
            
        self.recorder = VideoRecorder(
            output_dir=self.output_dir,
            camera=self.camera
        )
        
        # Motion settings
        self.record_seconds = MOTION_SETTINGS["record_seconds"]
        self.frame_diff_threshold = MOTION_SETTINGS["frame_diff_threshold"]
        self.motion_check_interval = MOTION_SETTINGS["motion_check_interval"]
        self.blur_size = MOTION_SETTINGS["blur_size"]
        self.threshold_value = MOTION_SETTINGS["threshold_value"]
        
        # Internal state
        self.prev_gray = None
        self.running = False
        
    def calculate_motion(self, frame):
        """Calculate motion score between current frame and previous frame.
        
        Args:
            frame: Current frame
            
        Returns:
            tuple: (motion_score, visualization_frame)
        """
        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, self.blur_size, 0)
        
        # Initialize prev_gray if not set
        if self.prev_gray is None:
            self.prev_gray = gray
            return 0, frame
            
        # Calculate frame difference
        frame_delta = cv2.absdiff(self.prev_gray, gray)
        thresh = cv2.threshold(frame_delta, self.threshold_value, 255, cv2.THRESH_BINARY)[1]
        motion_score = cv2.countNonZero(thresh)
        
        # Create visualization frame
        vis_frame = frame.copy()
        
        # Add motion score text
        cv2.putText(
            vis_frame,
            f"Motion: {motion_score}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0) if motion_score < self.frame_diff_threshold else (0, 0, 255),
            2
        )
        
        # Show motion detection visualization if significant motion
        if motion_score > self.frame_diff_threshold:
            # Highlight motion areas
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 50:  # Filter small noise
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(vis_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Update previous frame
        self.prev_gray = gray
        
        return motion_score, vis_frame
        
    def start_monitoring(self, show_preview=True):
        """Start monitoring for motion.
        
        Args:
            show_preview (bool): Show preview window
        """
        if not self.camera.cap or not self.camera.cap.isOpened():
            self.camera.open()
            
        self.running = True
        window_name = "Motion Detection" if show_preview else None
        
        print("🎥 Monitoring for motion...")
        print(f"Motion threshold: {self.frame_diff_threshold}")
        print(f"Record duration: {self.record_seconds} seconds")
        print("Press 'q' to quit")
        
        try:
            while self.running:
                # Read frame
                frame = self.camera.read()
                
                # Calculate motion
                motion_score, vis_frame = self.calculate_motion(frame)
                
                # Show preview
                if show_preview:
                    cv2.imshow(window_name, vis_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                        
                # Check for motion
                if motion_score > self.frame_diff_threshold:
                    print(f"📸 Motion detected! Score: {motion_score}")
                    self._record_motion_event()
                    
                # Wait between checks
                time.sleep(self.motion_check_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Exiting on keyboard interrupt.")
        finally:
            self.running = False
            if show_preview:
                cv2.destroyWindow(window_name)
                
    def _record_motion_event(self):
        """Record a motion event."""
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"motion_{timestamp}.mp4")
        
        print(f"📸 Recording for {self.record_seconds} seconds → {output_file}")
        
        # Record for specified duration
        self.recorder.record_duration(self.record_seconds)
        
        print("✅ Motion recording complete.")
        
    def stop(self):
        """Stop monitoring."""
        self.running = False