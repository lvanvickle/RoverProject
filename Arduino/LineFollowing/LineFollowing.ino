// Define the analog pins for each IR sensor
// These are connected to the IR sensors for reading the line status
int leftIRSensor = A0;      // Left IR sensor connected to analog pin A0
int centerIRSensor = A1;    // Center IR sensor connected to analog pin A1
int rightIRSensor = A2;     // Right IR sensor connected to analog pin A2

void setup() {
  // Initialize the sensor pins as input pins
  // This allows the Arduino to read values from the IR sensors
  pinMode(leftIRSensor, INPUT);
  pinMode(centerIRSensor, INPUT);
  pinMode(rightIRSensor, INPUT);

  // Start the serial communication to send data to the Raspberry Pi
  // 9600 baud rate is used for communication speed
  Serial.begin(9600);
}

void loop() {
  // Continuously send the sensor data as a comma-separated string
  // Format: "<leftSensorData>,<centerSensorData>,<rightSensorData>"
  Serial.print(getSensorData(leftIRSensor)); // Get data from left sensor and send it
  Serial.print(",");                         // Comma separates the values
  Serial.print(getSensorData(centerIRSensor)); // Get data from center sensor and send it
  Serial.print(",");
  Serial.print(getSensorData(rightIRSensor));  // Get data from right sensor and send it
  Serial.println();  // End the data line, making it easier to parse on the Raspberry Pi

  // Add a delay to stabilize readings and prevent spamming the serial connection
  delay(1000);
}

// Function to process analog sensor values into binary data (1 or 0)
// This simplifies interpreting the line-following status
int getSensorData(int sensor) {
  // Read the raw analog value from the sensor (0-1023 range)
  int sensorValue = analogRead(sensor);

  // Determine if the sensor is detecting a line
  // Line detected: return 1 (when value is below 500)
  // No line detected: return 0 (when value is above 500)
  if (sensorValue < 500) {
    return 1;  // Line detected
  } else {
    return 0;  // No line detected
  }
}