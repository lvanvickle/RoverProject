from utils.motors import move_forward, move_backward, turn_left, turn_right, stop_motors  # Motor control functions
import time  # For adding delays between motor actions

def test_motors():
    """
    Test the functionality of the motors by running them in different directions
    (forward, backward, left turn, right turn) at various speeds.
    """
    print("Testing motors...")  # Inform the user that testing is starting

    # Test forward movement
    print("Moving forward...")
    move_forward(0.8)  # Move forward at 80% speed
    time.sleep(2)  # Allow the rover to move forward for 2 seconds

    # Test backward movement
    print("Moving backward...")
    move_backward(0.8)  # Move backward at 80% speed
    time.sleep(2)  # Allow the rover to move backward for 2 seconds

    # Test left turn
    print("Turning left...")
    turn_left(0.8)  # Turn left at 80% speed
    time.sleep(2)  # Allow the rover to turn left for 2 seconds

    # Test right turn
    print("Turning right...")
    turn_right(0.8)  # Turn right at 80% speed
    time.sleep(2)  # Allow the rover to turn right for 2 seconds

    # Stop motors
    print("Stopping motors...")
    stop_motors()  # Stop all motors to ensure the rover comes to a complete stop

if __name__ == "__main__":
    """
    If the script is run directly, execute the motor test.
    """
    test_motors()  # Call the test_motors function