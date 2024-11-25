from adafruit_motorkit import MotorKit  # Library for controlling the Adafruit MotorHat

# Initialize the MotorHat
kit = MotorKit()  # Create an instance of MotorKit to control the motors

def validate_speed(speed):
    """
    Ensure the speed is within the valid range (0.0 to 1.0).
    Args:
        speed (float): Desired motor speed.
    Raises:
        ValueError: If the speed is outside the range [0.0, 1.0].
    """
    if not (0.0 <= speed <= 1.0):
        raise ValueError(f"Invalid speed {speed}. Speed must be between 0.0 and 1.0.")

def move_forward(speed=1.0):
    """
    Move all motors forward at the specified speed.
    Args:
        speed (float): Speed for the motors, from 0.0 (stop) to 1.0 (full speed).
    """
    validate_speed(speed)  # Ensure the speed is valid
    kit.motor1.throttle = speed  # Set motor 1 to move forward
    kit.motor2.throttle = speed  # Set motor 2 to move forward
    kit.motor3.throttle = speed  # Set motor 3 to move forward
    kit.motor4.throttle = speed  # Set motor 4 to move forward

def move_backward(speed=1.0):
    """
    Move all motors backward at the specified speed.
    Args:
        speed (float): Speed for the motors, from 0.0 (stop) to 1.0 (full speed).
    """
    validate_speed(speed)  # Ensure the speed is valid
    kit.motor1.throttle = -speed  # Set motor 1 to move backward
    kit.motor2.throttle = -speed  # Set motor 2 to move backward
    kit.motor3.throttle = -speed  # Set motor 3 to move backward
    kit.motor4.throttle = -speed  # Set motor 4 to move backward

def turn_left(speed=1.0):
    """
    Turn left by throttling the left motors at a lower speed or stopping them.
    Args:
        speed (float): Speed for the turning motors, from 0.0 (stop) to 1.0 (full speed).
    """
    validate_speed(speed)  # Ensure the speed is valid
    kit.motor1.throttle = speed  # Set motor 1 to move forward
    kit.motor2.throttle = 0.25  # Slow down or stop motor 2 for the turn
    kit.motor3.throttle = speed  # Set motor 3 to move forward
    kit.motor4.throttle = 0.25  # Slow down or stop motor 4 for the turn

def turn_right(speed=1.0):
    """
    Turn right by throttling the right motors at a lower speed or stopping them.
    Args:
        speed (float): Speed for the turning motors, from 0.0 (stop) to 1.0 (full speed).
    """
    validate_speed(speed)  # Ensure the speed is valid
    kit.motor1.throttle = 0.25  # Slow down or stop motor 1 for the turn
    kit.motor2.throttle = speed  # Set motor 2 to move forward
    kit.motor3.throttle = 0.25  # Slow down or stop motor 3 for the turn
    kit.motor4.throttle = speed  # Set motor 4 to move forward

def stop_motors():
    """
    Stop all motors by setting their throttle to 0.0.
    """
    kit.motor1.throttle = 0.0  # Stop motor 1
    kit.motor2.throttle = 0.0  # Stop motor 2
    kit.motor3.throttle = 0.0  # Stop motor 3
    kit.motor4.throttle = 0.0  # Stop motor 4