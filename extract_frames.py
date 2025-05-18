import cv2
import os

video_path = "videos/cat/chatty_video_2025-05-18_09-37-51.mp4"  # Change this!
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_rate = 5  # Save 1 frame every 5 frames

frame_count = 0
saved_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_rate == 0:
        filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1

    frame_count += 1

cap.release()
print(f"✅ Extracted {saved_count} frames to {output_dir}/")
