import cv2
import numpy as np

def detect_marker(frame, color="red"):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if color == "red":
        masks = [cv2.inRange(hsv, np.array([0,100,100]), np.array([10,255,255])), cv2.inRange(hsv, np.array([170,100,100]), np.array([180,255,255]))]
        mask = cv2.bitwise_or(*masks)
    elif color == "blue": mask = cv2.inRange(hsv, np.array([100,100,100]), np.array([130,255,255]))
    else: mask = cv2.inRange(hsv, np.array([0,100,100]), np.array([180,255,255]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = []
    for contour in contours:
        if cv2.contourArea(contour) < 200: continue
        moments = cv2.moments(contour)
        if moments["m00"]: points.append((int(moments["m10"]/moments["m00"]), int(moments["m01"]/moments["m00"])))
    return points
