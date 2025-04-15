import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import serial
import time
import mediapipe as mp
from collections import deque
import serial.tools.list_ports
import pyvirtualcam
from pyvirtualcam import PixelFormat

# === Settings ===
REQUESTED_WIDTH = 1920
REQUESTED_HEIGHT = 1080
FPS = 30
smooth_history = deque(maxlen=10)

# === Auto-detect Arduino port ===
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p.description or "CH340" in p.description:
            return p.device
    return None

port = find_arduino_port()
if port is None:
    #print("❌ Could not find Arduino. Make sure it's plugged in.")
    exit()

ser = serial.Serial(port, 9600)
time.sleep(2)

# === MediaPipe setup ===
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)

# === Camera setup ===
cap = cv2.VideoCapture(0)

# Request 1920x1080 (true 16:9 full HD)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, REQUESTED_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, REQUESTED_HEIGHT)

# Confirm actual resolution
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print(f"🖼️ Final camera resolution: {frame_width} x {frame_height}")
#print("Camera and Serial Ready.")

# === Virtual Camera Output ===
with pyvirtualcam.Camera(width=frame_width, height=frame_height, fps=FPS, fmt=PixelFormat.BGR) as cam:
    #print(f'🎥 Virtual camera started: {cam.device}')

    while True:
        ret, frame = cap.read()
        if not ret:
            #print("Can't receive frame. Exiting...")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        direction = "CENTER"
        frame_center_x = frame.shape[1] // 2
        margin = 250

        if results.detections:
            for detection in results.detections:
                box = detection.location_data.relative_bounding_box
                x = int(box.xmin * frame.shape[1])
                y = int(box.ymin * frame.shape[0])
                w = int(box.width * frame.shape[1])
                h = int(box.height * frame.shape[0])

                face_center_x = x + w // 2
                offset = face_center_x - frame_center_x

                if abs(offset) < margin:
                    direction = "CENTER"
                elif offset < 0:
                    direction = "LEFT"
                else:
                    direction = "RIGHT"
                break  # Track only first detected face

        # Smoothing direction
        smooth_history.append(direction)
        smoothed_direction = max(set(smooth_history), key=smooth_history.count)

        # Send to Arduino
        ser.write(smoothed_direction[0].encode())
        #print(f"Sent to Arduino: {smoothed_direction}")

        # Send to virtual webcam
        cam.send(frame)
        cam.sleep_until_next_frame()

# Cleanup
cap.release()
ser.close()
