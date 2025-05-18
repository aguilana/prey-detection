"""Camera capture functionality."""
import cv2
import os
import time
from datetime import datetime
from ..config.settings import VIDEO_SETTINGS, CAMERA_SETTINGS, PATHS

class Camera:
    """Camera capture class for video and image capture."""
    
    def __init__(self, camera_index=None):
        """Initialize the camera."""
        if camera_index is None:
            camera_index = CAMERA_SETTINGS["default_index"]
            
        self.camera_index = camera_index
        self.cap = None
        self.width = None
        self.height = None
        self.fps = VIDEO_SETTINGS["fps"]
        
    def __enter__(self):
        """Context manager entry point."""
        self.open()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.close()
        
    def open(self):
        """Open the camera."""
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Error: Could not open camera {self.camera_index}")
            
        # Get camera properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return self
        
    def close(self):
        """Close the camera."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            
    def read(self):
        """Read a frame from the camera."""
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("Camera is not open")
            
        ret, frame = self.cap.read()
        
        if not ret:
            raise RuntimeError("Could not read frame from camera")
            
        return frame
        
    def read_continuous(self, callback=None, window_name=None, exit_key='q'):
        """Read frames continuously until exit_key is pressed.
        
        Args:
            callback (callable): Function to call with each frame
            window_name (str): Window name for display
            exit_key (str): Key to exit the loop
        """
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("Camera is not open")
            
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Could not read frame")
                    break
                    
                if callback:
                    result = callback(frame)
                    # If callback returns False, break the loop
                    if result is False:
                        break
                
                if window_name:
                    cv2.imshow(window_name, frame)
                    
                    # Check for key press
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord(exit_key):
                        break
        finally:
            if window_name:
                cv2.destroyWindow(window_name)
                
    def get_properties(self):
        """Get camera properties."""
        return {
            "index": self.camera_index,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
        }
        
    def capture_image(self, output_path=None):
        """Capture a single image.
        
        Args:
            output_path (str): Path to save the image
            
        Returns:
            tuple: (frame, path) - The captured frame and path where saved
        """
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("Camera is not open")
            
        ret, frame = self.cap.read()
        
        if not ret:
            raise RuntimeError("Could not read frame from camera")
            
        if output_path:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, frame)
            
        return frame, output_path
        
    @staticmethod
    def list_cameras(max_cameras=5):
        """List available cameras.
        
        Args:
            max_cameras (int): Maximum number of cameras to check
            
        Returns:
            list: List of available camera indices
        """
        available_cameras = []
        
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
                
        return available_cameras