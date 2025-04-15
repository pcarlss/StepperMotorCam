# 🎯 Face Tracking Stepper Cam

A Python + Arduino project that tracks your face using a webcam and rotates a stepper motor in real-time to follow your movement. It also outputs the video feed to a **virtual webcam**, allowing integration with Zoom, OBS, Discord, and more.

## 📸 How It Works

- Uses **MediaPipe Face Detection** to locate your face in the webcam feed.
- Determines whether your face is on the LEFT, CENTER, or RIGHT side of the screen.
- Sends this directional data to an **Arduino** over serial communication.
- The Arduino rotates a **stepper motor** using the `Stepper` library to follow your face.
- A **virtual webcam** (via `pyvirtualcam`) mirrors the processed feed for use in other software.

## 🛠️ Features

- 🧠 Real-time face detection with noise smoothing
- 🔌 Auto-detects connected Arduino (CH340 or native)
- ⚙️ Smooth and consistent motor movement
- 📷 Virtual webcam output at Full HD (1080p @ 30 FPS)
- 📺 Easy to tweak and extend for your own setups

## 🧰 Requirements

### Python Side
- Python 3.10
- `opencv-python`
- `mediapipe`
- `pyserial`
- `pyvirtualcam`

Install the dependencies with:

```bash
pip install -r requirements.txt
```

### Arduino Side
- An Arduino Nano (or compatible board)
- Stepper motor (e.g., 28BYJ-48) and ULN2003 driver
- Stepper.h library (included by default in Arduino IDE)
- Upload the included Arduino sketch to your board.
- Keep the Arduino plugged into an available USB port

#### 🔌 Wiring
Connect your stepper motor to the Arduino as follows:
| Stepper Driver Pin     | Arduino Pin     |
|--------------|--------------|
| IN1 | D8| 
| IN2 | D10|
| IN3 | D9|
| IN4 | D11|

## ▶️ Running the Project
- Connect your stepper motor to the Arduino and upload the sketch.
- Plug in your webcam.
- Run the Python script: `python face_tracking_cam.py`
- A virtual webcam named something like OBS-Camera or PyVirtualCam will be available to use in Zoom, OBS, Discord, etc.

## 📅 Autostart on Windows
If you want the script to run automatically when you start your computer, you can add it to your Startup folder in Windows.

- Press Win + R to open the Run dialog.
- Type shell:startup and press Enter. This will open the Startup folder.
- Create a `.bat` (batch) file in this folder that runs your Python script. For example, you can create a file named face_tracking_start.bat with the following contents:
```
@echo off
cd /d "C:\path\to\your\project"
start "" "C:\path\to\your\Python310\pythonw.exe" python face_tracking_cam.py
```
## 🧪 Notes
- Adjust the margin value in the script to make tracking more or less sensitive.
- You can tune the step size and speed in the Arduino sketch for smoother movement.
