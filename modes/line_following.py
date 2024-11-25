import time
import serial
from utils.motors import move_forward, stop_motors, turn_left, turn_right

# Global variables
running = True  # Flag to indicate whether the line-following mode is active
ser = None  # Placeholder for the serial connection to the Arduino

def setup_serial():
    """
    Initialize serial communication with the Arduino for line following.
    Sets up a serial connection to read IR sensor data.
    """
    global ser
    try:
        # Attempt to connect to the Arduino on the specified serial port
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust '/dev/ttyUSB0' depending on setup
        print("Connected to Arduino for line following.")
        ser.reset_input_buffer()  # Flush the input buffer to clear old data
    except serial.SerialException as e:
        # Handle connection errors
        print(f"Error initializing serial communication: {e}")
        ser = None

def read_ir_sensors():
    """
    Read IR sensor data from the Arduino.
    The Arduino sends a comma-separated string of sensor values (e.g., "1,0,0").
    
    Returns:
        tuple: (left_sensor, center_sensor, right_sensor) as integers (0 or 1).
    """
    ser.reset_input_buffer()  # Clear any residual data before reading
    if ser and ser.in_waiting > 0:  # Check if data is available on the serial port
        try:
            # Read a line of data from the serial buffer
            data = ser.readline().decode().strip()  # Decode the byte data into a string
            sensor_values = data.split(',')  # Split the string into a list of sensor values
            if len(sensor_values) == 3:  # Ensure all three sensor values are present
                return int(sensor_values[0]), int(sensor_values[1]), int(sensor_values[2])
        except ValueError:
            # Handle errors in parsing sensor data
            print("Error parsing sensor data.")
    return None, None, None  # Return None if no valid data is received

def process_line_following_logic():
    """
    Core logic for line following using 3 IR sensors.
    - Reads sensor data from the Arduino.
    - Decides the movement of the rover based on the sensor values:
        - Center sensor detects the line: Move forward.
        - Left sensor detects the line: Turn left.
        - Right sensor detects the line: Turn right.
        - No sensors detect the line: Stop.
    """
    while running:  # Continue running as long as the mode is active
        # Get the sensor values from the Arduino
        left_sensor, center_sensor, right_sensor = read_ir_sensors()

        # Check if the sensor data is valid
        if left_sensor is None or center_sensor is None or right_sensor is None:
            print("No valid sensor data received. Stopping motors.")
            stop_motors()  # Stop the rover for safety
            time.sleep(0.1)  # Add a small delay before retrying
            continue

        # Process the sensor values to determine movement
        if center_sensor == 1:
            # Move forward if the line is centered
            move_forward(1)
        elif left_sensor == 1 and center_sensor == 0:
            # Turn left if the line is on the left
            turn_left(0.8)
        elif right_sensor == 1 and center_sensor == 0:
            # Turn right if the line is on the right
            turn_right(0.8)
        else:
            # Stop if no line is detected
            stop_motors()
        
        time.sleep(0.1)  # Add a small delay for stability

def start_line_following_mode():
    """
    Start the line-following mode.
    - Initializes the serial connection.
    - Starts processing the IR sensor data to control the rover.
    """
    global running
    running = True  # Set the running flag to True
    setup_serial()  # Initialize the serial connection with the Arduino

    if not ser:  # Check if the serial connection was successful
        print("Unable to start line-following mode due to serial connection issues.")
        return

    try:
        # Start the core logic for line following
        process_line_following_logic()
    except KeyboardInterrupt:
        # Handle interruptions gracefully (e.g., Ctrl+C)
        print("\nExiting line-following mode...")
    finally:
        # Ensure motors are stopped and clean up resources
        stop_motors()
        stop_line_following_mode()

def stop_line_following_mode():
    """
    Stop the line-following mode.
    - Stops the rover's motors.
    - Closes the serial connection to the Arduino.
    - Sets the running flag to False.
    """
    global running
    running = False  # Set the running flag to False to exit the loop
    if ser:  # Check if the serial connection is active
        ser.close()  # Close the serial connection
        print("Serial connection closed.")
    stop_motors()  # Ensure the motors are stopped
    print("Line-following mode stopped.")