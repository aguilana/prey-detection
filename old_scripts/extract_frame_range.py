import cv2
import os

# --- Settings ---
video_path = "videos/cat/chatty_video_2025-05-17_14-16-50.mp4"  # change this
output_dir = "frames/cat"
start_sec = 8
end_sec = 12
frame_interval = 5  # Save every Nth frame

# --- Setup ---
os.makedirs(output_dir, exist_ok=True)
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    print("❌ Error: Could not retrieve FPS from video.")
    exit()
print(f"🎥 Video FPS: {fps}")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

start_frame = int(start_sec * fps)
end_frame = int(end_sec * fps)

print(f"🎯 Video FPS: {fps}")
print(f"🎯 Total frames: {total_frames}")
print(f"🎯 Duration: {duration:.2f} sec")
print(
    f"🎯 Extracting frames from {start_sec}s to {end_sec}s ({start_frame}–{end_frame})"
)

frame_count = 0
saved = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret or frame_count > end_frame:
        break

    if frame_count >= start_frame and (frame_count % frame_interval == 0):
        filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        saved += 1

    frame_count += 1

cap.release()
print(f"✅ Saved {saved} frames to {output_dir}/")
