"""HoloMat-style camera/projector demo.

Tracks red and blue objects, projects a simple dashboard, and measures the
first two detected markers. This is deliberately a demo, not a calibration
system: pixel distance is reported until a real-world scale is supplied.
"""
import argparse
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cv2
from vision.holo_marker import detect_marker

def draw_button(frame, label, x, y, active=False):
    color = (70, 170, 255) if active else (55, 75, 105)
    cv2.rectangle(frame, (x, y), (x + 150, y + 42), color, -1)
    cv2.putText(frame, label, (x + 16, y + 28), cv2.FONT_HERSHEY_SIMPLEX, .65, (245, 250, 255), 2)

def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--camera", type=int, default=int(os.getenv("CAMERA_INDEX", 0))); parser.add_argument("--display", type=int, default=int(os.getenv("PROJECTOR_DISPLAY_INDEX", 1)))
    args = parser.parse_args(); camera = cv2.VideoCapture(args.camera)
    if not camera.isOpened(): raise SystemExit(f"Could not open camera {args.camera}")
    ruler = True; window = "Ultron HoloMat Projection"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL); cv2.resizeWindow(window, int(os.getenv("PROJECTOR_WIDTH", 1280)), int(os.getenv("PROJECTOR_HEIGHT", 720)))
    try:
        while True:
            ok, frame = camera.read()
            if not ok: break
            red, blue = detect_marker(frame, "red"), detect_marker(frame, "blue"); points = red + blue
            for point, color in zip(red, [(0, 80, 255)] * len(red)):
                cv2.circle(frame, point, 16, color, 3)
            for point in blue: cv2.circle(frame, point, 16, (255, 100, 30), 3)
            overlay = frame.copy(); cv2.rectangle(overlay, (0, 0), (240, 110), (6, 12, 23), -1); frame = cv2.addWeighted(overlay, .82, frame, .18, 0)
            draw_button(frame, "RULER ON" if ruler else "RULER OFF", 15, 15, ruler); draw_button(frame, "CLEAR (C)", 15, 62)
            cv2.putText(frame, f"Objects tracked: {len(points)}", (270, 35), cv2.FONT_HERSHEY_SIMPLEX, .8, (225, 240, 255), 2)
            if ruler and len(points) >= 2:
                a, b = points[0], points[1]; distance = ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** .5
                cv2.line(frame, a, b, (80, 255, 180), 3); mid = ((a[0]+b[0])//2, (a[1]+b[1])//2)
                cv2.putText(frame, f"{distance:.0f} px", mid, cv2.FONT_HERSHEY_SIMPLEX, .8, (80,255,180), 2)
            cv2.putText(frame, "Q quit   M ruler   C clear", (15, frame.shape[0]-18), cv2.FONT_HERSHEY_SIMPLEX, .6, (180,200,220), 1)
            cv2.imshow(window, frame); key = cv2.waitKey(1) & 0xff
            if key == ord('q'): break
            if key == ord('m'): ruler = not ruler
            if key == ord('c'): points.clear()
    finally: camera.release(); cv2.destroyAllWindows()
if __name__ == "__main__": main()
