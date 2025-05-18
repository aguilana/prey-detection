"""Configuration settings for the prey detection system."""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Video settings
VIDEO_SETTINGS = {
    "codec": "mp4v",
    "extension": ".mp4",
    "fps": 20.0,
    "resolution": (640, 480),
}

# File paths
PATHS = {
    "videos_dir": os.path.join(BASE_DIR, "videos"),
    "cat_videos_dir": os.path.join(BASE_DIR, "videos", "cat"),
    "human_videos_dir": os.path.join(BASE_DIR, "videos", "human"),
    "motion_videos_dir": os.path.join(BASE_DIR, "videos", "motion"),
    "frames_dir": os.path.join(BASE_DIR, "frames"),
    "models_dir": os.path.join(BASE_DIR, "models"),
}

# Create directories if they don't exist
for path in PATHS.values():
    os.makedirs(path, exist_ok=True)

# Motion detection settings
MOTION_SETTINGS = {
    "record_seconds": 15,
    "frame_diff_threshold": 100000,
    "motion_check_interval": 1,
    "blur_size": (21, 21),
    "threshold_value": 25,
}

# Detection model settings
MODEL_SETTINGS = {
    "confidence_threshold": 0.5,
    "nms_threshold": 0.4,
    "input_size": (416, 416),
}

# Camera settings
CAMERA_SETTINGS = {
    "default_index": 0,
}