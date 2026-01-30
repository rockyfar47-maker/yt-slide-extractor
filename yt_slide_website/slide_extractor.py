import cv2, os, subprocess, numpy as np

def extract_slides(youtube_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run(
        ["yt-dlp", "-f", "mp4", "-o", "video.mp4", youtube_url],
        check=True
    )

    cap = cv2.VideoCapture("video.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_gap = fps * 1

    prev_gray = None
    frame_index = 0
    slide_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_gap != 0:
            frame_index += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            if np.mean(diff) < 5:
                frame_index += 1
                continue

        slide_count += 1
        cv2.imwrite(f"{output_dir}/slide_{slide_count}.jpg", frame)
        prev_gray = gray
        frame_index += 1

    cap.release()
