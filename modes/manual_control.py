import pygame  # For joystick input handling
from utils.motors import move_forward, move_backward, turn_left, turn_right, stop_motors  # Motor control functions
import time  # For adding delays to prevent overloading the CPU

# Define speed settings
FAST_SPEED = 1.0  # Full speed for the rover
SLOW_SPEED = 0.8  # Slower speed for precise movements
current_speed = SLOW_SPEED  # Start with slow speed by default

# Flag to track whether the manual control mode is running
running = True

def start_manual_control():
    """
    Start joystick-based manual control of the rover.
    This function initializes the joystick and allows the user to control
    the rover's movement and speed using joystick inputs.
    """
    global running, current_speed
    pygame.init()  # Initialize all imported Pygame modules

    # Check if a joystick is connected
    if pygame.joystick.get_count() == 0:
        print("No joystick detected. Exiting manual control mode.")
        return

    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Detected joystick: {joystick.get_name()}")  # Print the joystick name for confirmation

    # Deadzone threshold to ignore small joystick movements
    deadzone = 0.25
    speed_toggle_pressed = False  # Prevent rapid toggling of speed

    try:
        while running:
            pygame.event.pump()  # Process all joystick events

            # Handle speed toggle (X on PS5 controller or equivalent)
            if joystick.get_button(0):  # Get state of button
                if not speed_toggle_pressed:  # Ensure toggle happens only once per button press
                    # Toggle between fast and slow speeds
                    current_speed = FAST_SPEED if current_speed == SLOW_SPEED else SLOW_SPEED
                    print(f"Speed toggled to: {'FAST' if current_speed == FAST_SPEED else 'SLOW'}")
                    speed_toggle_pressed = True
            else:
                speed_toggle_pressed = False  # Reset toggle state when button is released

            # Get joystick axis input for turning
            axis_x = joystick.get_axis(0)  # Horizontal axis (left joystick for turning)

            # Handle forward and backward movement using triggers
            if joystick.get_button(7):  # Right trigger pressed (Forward)
                move_forward(current_speed)
            elif joystick.get_button(6):  # Left trigger pressed (Backward)
                move_backward(current_speed)
            elif abs(axis_x) > deadzone:  # Turning when joystick is moved left or right
                if axis_x > 0:  # Turn right
                    turn_right(current_speed)
                elif axis_x < 0:  # Turn left
                    turn_left(current_speed)
            else:
                stop_motors()  # Stop motors when joystick is neutral

            time.sleep(0.01)  # Add a small delay to prevent CPU overload

    except KeyboardInterrupt:
        # Stop the rover safely if the user interrupts (e.g., Ctrl+C)
        stop_motors()
        print("\nExiting manual control mode...")

def stop_manual_control():
    """
    Safely stop the manual control mode.
    Sets the running flag to False and stops the rover motors.
    """
    global running
    running = False  # Stop the main control loop
    stop_motors()  # Ensure the rover stops
    print("Manual control mode stopped.")
