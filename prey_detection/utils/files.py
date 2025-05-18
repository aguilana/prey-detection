"""File utilities for managing media files."""
import os
import glob
import shutil
from pathlib import Path
from datetime import datetime
from ..config.settings import PATHS

def list_video_files(directory=None, pattern="*.mp4", recursive=False):
    """List video files in a directory.
    
    Args:
        directory (str): Directory to search
        pattern (str): File pattern to match
        recursive (bool): Search subdirectories
        
    Returns:
        list: List of video file paths
    """
    if directory is None:
        directory = PATHS["videos_dir"]
        
    search_pattern = os.path.join(directory, "**" if recursive else "", pattern)
    video_files = glob.glob(search_pattern, recursive=recursive)
    
    return sorted(video_files)
    
def get_video_info(video_path):
    """Get information about a video file.
    
    Args:
        video_path (str): Path to video file
        
    Returns:
        dict: Video information
    """
    file_stats = os.stat(video_path)
    file_path = Path(video_path)
    
    return {
        "filename": file_path.name,
        "path": str(file_path),
        "size_bytes": file_stats.st_size,
        "size_mb": file_stats.st_size / (1024 * 1024),
        "created": datetime.fromtimestamp(file_stats.st_ctime),
        "modified": datetime.fromtimestamp(file_stats.st_mtime),
        "extension": file_path.suffix,
    }
    
def create_directory_structure():
    """Create standard directory structure for the project."""
    for path in PATHS.values():
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")
        
def organize_videos_by_date(source_dir=None, target_base_dir=None):
    """Organize videos by date (YYYY-MM-DD folders).
    
    Args:
        source_dir (str): Source directory
        target_base_dir (str): Target base directory
        
    Returns:
        dict: Statistics about the operation
    """
    if source_dir is None:
        source_dir = PATHS["videos_dir"]
        
    if target_base_dir is None:
        target_base_dir = os.path.join(PATHS["videos_dir"], "organized")
        
    # Create target directory
    os.makedirs(target_base_dir, exist_ok=True)
    
    # Find all video files
    video_patterns = ["*.mp4", "*.avi", "*.mov"]
    video_files = []
    
    for pattern in video_patterns:
        video_files.extend(glob.glob(os.path.join(source_dir, pattern)))
        
    # Organize statistics
    stats = {
        "total_files": len(video_files),
        "organized_files": 0,
        "skipped_files": 0,
        "created_folders": set(),
    }
    
    # Process each file
    for video_file in video_files:
        # Get file info
        file_info = get_video_info(video_file)
        file_date = file_info["modified"].strftime("%Y-%m-%d")
        
        # Create date folder
        date_folder = os.path.join(target_base_dir, file_date)
        os.makedirs(date_folder, exist_ok=True)
        stats["created_folders"].add(date_folder)
        
        # Copy file to date folder
        target_path = os.path.join(date_folder, os.path.basename(video_file))
        
        if os.path.exists(target_path):
            print(f"File already exists: {target_path}")
            stats["skipped_files"] += 1
            continue
            
        shutil.copy2(video_file, target_path)
        stats["organized_files"] += 1
        print(f"Copied: {video_file} -> {target_path}")
        
    # Convert set to list for easier serialization
    stats["created_folders"] = list(stats["created_folders"])
    
    return stats