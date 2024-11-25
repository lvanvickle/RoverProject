# **Raspberry Pi Rover Project**

## **Overview**
This project is a multi-functional rover controlled by a Raspberry Pi and Arduino. It includes several operational modes such as manual control, obstacle avoidance, line following, and face detection/recognition. The project was undertaken to learn and experiment
in the field of robotics.

---

## **Features**
- **Manual Control**:
  - Control the rover using a joystick or controller.
- **Obstacle Avoidance**:
  - Uses an ultrasonic sensor to detect and avoid obstacles.
- **Line Following**:
  - Follows a predefined path using infrared sensors.
- **Face Detection and Recognition**:
  - Identifies faces using a camera feed and pre-trained encodings.

---

## **Hardware Requirements**
  - Junior Runt Rover Chassis: Provides the base for the rover, housing the motors and other components.
  - Adafruit DC & Stepper Motor HAT for Raspberry Pi: Controls the DC motors and integrates with the Raspberry Pi.
  - GPIO Stacking Header for Pi
  - Extra long 2x20 pins: Allows additional components to connect to the Raspberry Pi.
  - Assembled Pi T-Cobbler Plus (GPIO Breakout): Breaks out the GPIO pins for easy prototyping on a breadboard.
  - Raspberry Pi 4 Model B (4GB RAM): Acts as the primary control board for the rover.
  - Arduino Uno Rev 3: Handles obstacle avoidance and line-following logic.
  - USB Battery Pack: Powers the Raspberry Pi
  - 4xAA Battery Holder with On/Off switch: Powers the motors and additional hardware.
  - Half-size Breadboard: Used for prototyping and connecting components.
  - Ultrasonic Sensor (HC-SR04): Detects obstacles for autonomous navigation.
  - 3xIR Sensors: Tracks the line for the line-following mode.
  - Continuous Servo: Rotates the ultrasonic sensor for scanning.
  - Jumper Wires: Connect various components.
  - USB-A to USB-B Cable: Connects the Arduino to the Raspberry Pi or a computer.
  - Web Cam: Captures live video feed for streaming or face recognition.
  - Joystick (tested with PS5 controller): Provides manual control for the rover.

---

## **Project Structure**
```plaintext
.
├── main.py                 # Main script to run the application
├── modes/                  # Operational modes
│   ├── manual_control.py   # Joystick-based manual control
│   ├── obstacle_avoidance.py # Ultrasonic-based obstacle avoidance
│   ├── line_following.py   # IR sensor-based line following
├── utils/                  # Utility scripts
│   ├── motors.py           # Motor control logic
│   ├── camera.py           # Camera feed and face detection logic
│   └── haarcascades/       # Haarcascade files for face detection
│       └── haarcascade_frontalface_default.xml
├── data/                   # Face data and encodings
│   ├── face_encodings.py   # Script for generating face encodings
│   ├── face_encodings.json # Pre-generated face encodings
│   └── sample_faces/       # Sample face images
├── tests/                  # Test scripts
│   └── test_motors.py      # Script for testing motor functionality
└── requirements.txt        # Python dependencies
