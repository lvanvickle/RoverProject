# Import statements for premade modules
import threading  # Allows us to run modes concurrently in separate threads
import tkinter as tk  # Provides the GUI framework
from tkinter import messagebox  # Displays notification pop-ups in the GUI
import ttkbootstrap as ttk  # Modern GUI library based on tkinter
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER  # Predefined design themes for GUI components
from PIL import Image, ImageTk  # Handles video frame processing for displaying in the GUI
from multiprocessing import Process, Queue, Value  # Manages separate processes for the camera stream and face recognition

# Import statements for custom modules
from utils.motors import stop_motors  # Provides functions to control and stop the rover motors
from modes.manual_control import start_manual_control, stop_manual_control  # Manual control mode logic
from modes.obstacle_avoidance import start_autonomous_mode, stop_autonomous_mode  # Obstacle avoidance mode logic
from modes.line_following import start_line_following_mode, stop_line_following_mode  # Line following mode logic
from utils.camera import camera_stream  # Handles camera feed functionality

# Global variables
current_thread = None  # Keeps track of the currently active thread for mode execution
current_mode = None  # Keeps track of the currently active mode
face_recognition_process = None  # Tracks the process running face recognition (if used)
frame_queue = Queue(maxsize=10)  # Queue to store video frames for the camera stream
camera_mode = Value('i', 0)  # Shared value to toggle between simple camera stream and face detection
camera_process = None  # Tracks the process running the camera stream

# Function to stop the current mode
def stop_current_mode():
    """
    Stops any currently running mode by terminating its thread and resetting the state.
    """
    global current_thread, current_mode
    if current_thread and current_thread.is_alive():
        # Stop the appropriate mode based on the current mode
        if current_mode == "manual":
            stop_manual_control()
        elif current_mode == "autonomous":
            stop_autonomous_mode()
        elif current_mode == "line_following":
            stop_line_following_mode()
        
        # Wait for the thread to finish
        current_thread.join()
        current_thread = None
        current_mode = None
        stop_motors()  # Ensure all motors are stopped for safety

# Function to start a new mode
def start_mode(mode_name, mode_function):
    """
    Stops the current mode (if any) and starts the specified mode in a new thread.
    """
    global current_thread, current_mode
    stop_current_mode()  # Ensure no other mode is running
    current_mode = mode_name
    current_thread = threading.Thread(target=mode_function)  # Create a thread for the new mode
    current_thread.start()  # Start the mode thread

# GUI functions to handle mode switching
def switch_to_manual():
    """
    Switch to manual control mode.
    """
    start_mode("manual", start_manual_control)

def switch_to_autonomous():
    """
    Switch to obstacle avoidance mode.
    """
    start_mode("autonomous", start_autonomous_mode)

def switch_to_line_following():
    """
    Switch to line following mode.
    """
    start_mode("line_following", start_line_following_mode)

# Camera-related functions
def start_camera_stream():
    """
    Starts the camera stream in a separate process.
    """
    global camera_process
    if camera_process and camera_process.is_alive():
        print("Camera stream is already running.")
        return

    camera_process = Process(target=camera_stream, args=(camera_mode,))  # Start the camera stream process
    camera_process.start()

def stop_camera_stream():
    """
    Stops the camera stream process if it is running.
    """
    global camera_process
    if camera_process and camera_process.is_alive():
        camera_process.terminate()
        camera_process.join()  # Wait for the process to fully stop
        print("Camera stream stopped.")

def toggle_camera_mode():
    """
    Toggles between the simple camera stream (0) and face detection mode (1).
    """
    camera_mode.value = 1 if camera_mode.value == 0 else 0  # Toggle the camera mode
    mode_name = "Face Detection" if camera_mode.value == 1 else "Simple Stream"
    print(f"Camera mode switched to: {mode_name}")

# Set up the GUI
root = ttk.Window(themename="darkly")  # Create a themed GUI window
root.title("Rover Control")  # Set the window title

# Create a label for displaying the video feed
camera_label = ttk.Label(root)  # Placeholder for the video feed
camera_label.grid(row=0, column=1, padx=10, pady=10)  # Position the video feed in the GUI

# Create buttons for the GUI
manual_button = ttk.Button(root, text="Manual Control", width=20, command=switch_to_manual)  # Button for manual mode
autonomous_button = ttk.Button(root, text="Autonomous Mode", width=20, command=switch_to_autonomous)  # Button for obstacle avoidance mode
line_follow_button = ttk.Button(root, text="Line Following Mode", width=20, command=switch_to_line_following)  # Button for line following mode
start_cam_button = ttk.Button(root, text="Start Camera", command=start_camera_stream)  # Button to start the camera stream
stop_cam_button = ttk.Button(root, text="Stop Camera", command=stop_camera_stream)  # Button to stop the camera stream
toggle_cam_button = ttk.Button(root, text="Toggle Camera Mode", command=toggle_camera_mode)  # Button to toggle between camera modes

# Layout the buttons in the grid
manual_button.grid(row=0, column=0, padx=10, pady=10)  # Place the manual mode button
autonomous_button.grid(row=1, column=0, padx=10, pady=10)  # Place the obstacle avoidance button
line_follow_button.grid(row=2, column=0, padx=10, pady=10)  # Place the line following button
start_cam_button.grid(row=5, column=0, padx=10, pady=10)  # Place the start camera button
stop_cam_button.grid(row=5, column=1, padx=10, pady=10)  # Place the stop camera button
toggle_cam_button.grid(row=5, column=2, padx=10, pady=10)  # Place the toggle camera mode button

# Start the main loop
root.mainloop()  # Run the GUI loop, allowing the user to interact with the interface
