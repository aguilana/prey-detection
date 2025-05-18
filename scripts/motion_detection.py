import cv2
import os
from datetime import datetime
import time

# --- Settings ---
RECORD_SECONDS = 15
FRAME_DIFF_THRESHOLD = 100000  # Tune this based on sensitivity
MOTION_CHECK_INTERVAL = 1  # seconds between motion checks
OUTPUT_FOLDER = "videos/motion"
VIDEO_INDEX = 0

# --- Setup ---
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
cap = cv2.VideoCapture(VIDEO_INDEX)

if not cap.isOpened():
    print(f"❌ Cannot open webcam at index {VIDEO_INDEX}.")
    exit()

print("🎥 Watching for motion...")

# Read first frame
ret, prev_frame = cap.read()
if not ret:
    print("❌ Could not read initial frame.")
    cap.release()
    exit()

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

try:
    while True:
        time.sleep(MOTION_CHECK_INTERVAL)

        ret, frame = cap.read()
        if not ret:
            print("❌ Could not read initial frame. Is the camera available?")
            cap.release()
            exit()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Frame difference
        frame_delta = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_score = cv2.countNonZero(thresh)

        print(f"Motion Score: {motion_score}")

        if motion_score > FRAME_DIFF_THRESHOLD:
            # Start recording
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = os.path.join(OUTPUT_FOLDER, f"motion_{timestamp}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

            print(
                f"📸 Motion detected! Recording for {RECORD_SECONDS} seconds → {video_path}"
            )
            start_time = time.time()

            while time.time() - start_time < RECORD_SECONDS:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                cv2.imshow("Recording", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("🔴 Stopped early.")
                    break

            out.release()
            cv2.destroyWindow("Recording")
            print("✅ Done recording.\n")

        prev_gray = gray

except KeyboardInterrupt:
    print("\n👋 Exiting on keyboard interrupt.")

cap.release()
cv2.destroyAllWindows()
