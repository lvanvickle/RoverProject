#include <Servo.h>

// Initialize pins for the ultrasonic sensor and servo motor
int trigPin = 9;  // Ultrasonic sensor trigger pin
int echoPin = 10; // Ultrasonic sensor echo pin
int servoPin = 6; // Servo control pin

// Create a Servo object to control the continuous servo
Servo servo;

// Minimum distance threshold for the rover to stop and decide a new direction
int safeDistance = 25; // Distance in centimeters

void setup() {
  // Start serial communication to send data to the Raspberry Pi
  Serial.begin(9600);

  // Attach the servo to its control pin
  servo.attach(servoPin);

  // Configure the ultrasonic sensor pins
  pinMode(trigPin, OUTPUT); // Trigger pin sends pulses
  pinMode(echoPin, INPUT);  // Echo pin receives the reflected pulse
}

void loop() {
  // Make sure the servo is stopped
  servo.write(90);  // Stop servo
  delay(500);       // Allow the servo to settle

  // Measure the distance directly in front of the rover
  int distance = measureDistance();

  // Check if the measured distance is below the safe threshold
  if (distance < safeDistance) {
    // Obstacle detected - scan to find a clear path
    const char* bestDirection = scanForClearPath();

    // Send the chosen direction to the Raspberry Pi
    Serial.println(bestDirection);
  } else {
    // No obstacle detected - path ahead is clear
    Serial.println("Clear");
  }

  // Small delay to avoid excessive processing
  delay(1000);
}

// Function to measure distance using the ultrasonic sensor
int measureDistance() {
  // Send a 10-microsecond pulse to the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the duration of the echo pulse in microseconds
  long duration = pulseIn(echoPin, HIGH);

  // Calculate distance in centimeters
  // Speed of sound = 343 m/s, so distance = (duration * 0.034) / 2
  int distance = duration * 0.034 / 2;
  return distance;
}

// Function to scan left, back, and right for the best clear path
const char* scanForClearPath() {
  int checkTime = 300; // Time (ms) to move the servo to each position
  int distance = 0;    // Variable to hold measured distances

  // Scan left
  servo.write(0);        // Move the servo counterclockwise (left)
  delay(checkTime);      // Wait for the servo to reach position
  servo.write(90);       // Stop the servo
  delay(500);            // Allow the servo to stabilize
  distance = measureDistance(); // Measure the distance on the left
  if (distance > safeDistance) {
    // Return to center if left is clear
    servo.write(125);    // Move back to center
    delay(checkTime);
    servo.write(90);     // Stop the servo
    return "L";          // Return "L" for left
  }

  // Scan back
  servo.write(0);        // Continue moving counterclockwise (back)
  delay(checkTime);      // Wait for the servo to reach position
  servo.write(90);       // Stop the servo
  delay(500);            // Allow the servo to stabilize
  distance = measureDistance(); // Measure the distance at the back
  if (distance > safeDistance) {
    // Return to center if back is clear
    servo.write(125);    // Move back to center
    delay(2 * checkTime); // Adjust delay for back position
    servo.write(90);     // Stop the servo
    return "B";          // Return "B" for back
  }

  // Scan right
  servo.write(0);        // Continue moving counterclockwise (right)
  delay(checkTime);      // Wait for the servo to reach position
  servo.write(90);       // Stop the servo
  delay(500);            // Allow the servo to stabilize
  distance = measureDistance(); // Measure the distance on the right
  if (distance > safeDistance) {
    // Return to center if right is clear
    servo.write(125);    // Move back to center
    delay(3 * checkTime); // Adjust delay for right position
    servo.write(90);     // Stop the servo
    return "R";          // Return "R" for right
  }

  // No clear path found - return to center position
  servo.write(125);      // Move back to center
  delay(3 * checkTime);  // Allow the servo to reposition
  servo.write(90);       // Stop the servo
  return "Obstructed";   // Indicate that no clear path was found
}