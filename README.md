# Prey Detection

A computer vision system for detecting cats with prey in video footage.
The end goal of this project is more or less to be able to fine-tune a model (e.g., YOLOv8) to detect prey (mice, birds, etc) in videos of cats.
Eventually would like to connect this to Raspberry Pi and have it run in real-time on a camera feed to control
a cat door or something similar.

This project is a work in progress and is not yet fully functional.

## Overview

This project allows you to:

1. Capture video footage of your cat
2. Extract video frames for analysis
3. Detect motion and automatically record
4. Process frames for model training (e.g., YOLOv8)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/prey_detection.git
   cd prey_detection
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```
   pip install -e .
   ```

## Usage

### Recording Video

The system provides two ways to record video:

1. Interactive mode (start/stop recording with keypress):

   ```
   python scripts/record_video.py
   ```

2. Record for a specific duration:
   ```
   python scripts/record_video.py --duration 60  # Record for 60 seconds
   ```

Commands during interactive recording:

- `r`: Start/stop recording
- `q`: Quit
- `Space`: Take a screenshot

### Motion Detection

Automatically detect motion and record when triggered:

```
python scripts/motion_detect.py
```

Options:

- `--threshold 50000`: Set motion sensitivity
- `--duration 10`: Record for 10 seconds when motion detected
- `--interval 0.5`: Check for motion every 0.5 seconds

### Extracting Frames

Extract frames from videos for analysis or training:

```
python scripts/extract_frames.py videos/cat/video_2025-05-17.mp4 --interval 5
```

Options:

- `--interval 5`: Extract every 5th frame
- `--start-time 10 --end-time 30`: Extract frames between 10s and 30s
- `--start-frame 100 --end-frame 200`: Extract specific frame range
- `--output-dir frames/my_dataset`: Specify output location

## Project Structure

```
prey_detection/
├── prey_detection/        # Main package
│   ├── capture/           # Video capture modules
│   ├── processing/        # Video processing
│   ├── utils/             # Utility functions
│   ├── models/            # ML models (for future)
│   └── config/            # Configuration settings
├── scripts/               # Command-line scripts
├── videos/                # Video storage
│   ├── cat/               # Cat videos
│   ├── human/             # Human videos (for comparison/testing)
│   └── motion/            # Motion-triggered videos
└── frames/                # Extracted frames
```

## Future Enhancements

- YOLOv8 integration for prey detection
- Real-time prey alerts
- Web interface for viewing footage
- Cloud storage and analysis

## License

MIT
