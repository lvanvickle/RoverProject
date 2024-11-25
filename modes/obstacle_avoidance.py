import time  # For delays and timing logic
import serial  # For serial communication with the Arduino
from utils.motors import move_forward, move_backward, stop_motors, turn_left, turn_right  # Motor control functions

# Global variables
running = True  # Flag to indicate whether the autonomous mode is active
ser = None  # Placeholder for the serial connection to the Arduino

def setup_serial():
    """
    Initialize serial communication with the Arduino.
    Establishes a connection to read direction commands for obstacle avoidance.
    """
    global ser
    try:
        # Attempt to connect to the Arduino on the specified serial port
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust '/dev/ttyUSB0' depending on setup
        print("Connected to Arduino for obstacle avoidance.")
        ser.reset_input_buffer()  # Flush the input buffer to clear old data
    except serial.SerialException as e:
        # Handle connection errors
        print(f"Error initializing serial communication: {e}")
        ser = None

def read_direction():
    """
    Read direction data from the Arduino.
    The Arduino sends direction commands as strings (e.g., "L", "R", "Clear").
    
    Returns:
        str: Direction command from the Arduino, or None if no valid data is received.
    """
    ser.reset_input_buffer()  # Clear any residual data before reading
    if ser and ser.in_waiting > 0:  # Check if data is available on the serial port
        try:
            # Read a line of data from the serial buffer
            data = ser.readline().decode().strip()  # Decode the byte data into a string
            return data  # Return the received direction
        except Exception as e:
            # Handle errors during serial communication
            print(f"Error reading from serial: {e}")
    return None  # Return None if no valid data is received

def process_autonomous_logic():
    """
    Core logic for obstacle avoidance.
    - Reads direction commands from the Arduino.
    - Executes motor actions based on the commands:
        - "Clear": Move forward.
        - "L": Turn left.
        - "R": Turn right.
        - "B": Move backward.
        - "Obstructed": Stop and wait.
    """
    while running:  # Continue running as long as the mode is active
        direction = read_direction()  # Get the direction command from the Arduino

        # Process the received direction and execute the corresponding action
        if direction == "Clear":
            move_forward(1)  # Move forward at full speed
            time.sleep(0.5)  # Maintain forward movement for a short duration
        elif direction == "L":
            stop_motors()  # Stop first before turning
            turn_left(0.8)  # Turn left at 80% speed
            time.sleep(0.5)  # Delay for turning
        elif direction == "R":
            stop_motors()  # Stop first before turning
            turn_right(0.8)  # Turn right at 80% speed
            time.sleep(0.5)  # Delay for turning
        elif direction == "B":
            stop_motors()  # Stop first before reversing
            move_backward(0.8)  # Move backward at 80% speed
            time.sleep(0.5)  # Delay for reversing
        elif direction == "Obstructed":
            stop_motors()  # Stop all motors
            print("Obstacle detected in all directions. Waiting...")
            time.sleep(0.5)  # Pause to allow the Arduino to reevaluate the surroundings
        else:
            # Handle unknown or invalid commands
            stop_motors()
            print("Unknown direction received, stopping motors.")

def start_autonomous_mode():
    """
    Start the obstacle avoidance mode.
    - Initializes the serial connection.
    - Runs the main obstacle avoidance logic.
    """
    global running
    running = True  # Set the running flag to True
    setup_serial()  # Initialize the serial connection with the Arduino

    if not ser:  # Check if the serial connection was successfully established
        print("Unable to start autonomous mode due to serial connection issues.")
        return

    try:
        # Start processing the obstacle avoidance logic
        process_autonomous_logic()
    except KeyboardInterrupt:
        # Handle interruptions gracefully (e.g., Ctrl+C)
        print("\nExiting autonomous mode...")
    finally:
        # Ensure motors are stopped and clean up resources
        stop_motors()
        stop_autonomous_mode()

def stop_autonomous_mode():
    """
    Stop the obstacle avoidance mode.
    - Stops the rover's motors.
    - Closes the serial connection to the Arduino.
    - Sets the running flag to False.
    """
    global running
    running = False  # Set the running flag to False to exit the loop
    if ser:  # Check if the serial connection is active
        ser.close()  # Close the serial connection
        print("Serial connection closed.")
    stop_motors()  # Ensure all motors are stopped
    print("Autonomous mode stopped.")
