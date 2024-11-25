import cv2  # OpenCV library for camera and image processing
from multiprocessing import Process, Value  # For running processes and shared variables
import face_recognition  # Library for face detection and recognition
import json  # For loading and parsing face encodings from a JSON file

def simple_camera_feed():
    """
    Display a simple live camera feed without any additional processing.
    Opens the default camera and streams the video feed in a window.
    """
    cap = cv2.VideoCapture(0)  # Open the default camera (index 0)
    if not cap.isOpened():  # Check if the camera is accessible
        print("Error: Could not open camera.")
        return

    try:
        while True:
            # Capture a single frame from the camera
            ret, frame = cap.read()
            if not ret:  # Handle frame capture errors
                print("Error: Could not read frame.")
                break

            # Display the frame in a window
            cv2.imshow("Camera Stream", frame)

            # Exit the loop if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release the camera resource and close the display window
        cap.release()
        cv2.destroyAllWindows()

def face_detection_feed(known_faces_file="face_encodings.json"):
    """
    Display a live camera feed with face detection and recognition.
    - Detects faces in the camera feed and compares them against known encodings.
    - Annotates the video stream with bounding boxes and names of recognized faces.

    Args:
        known_faces_file (str): Path to the JSON file containing known face encodings.
    """
    # Load known face encodings and names from the provided JSON file
    known_names, known_encodings = [], []
    try:
        with open(known_faces_file, "r") as f:
            data = json.load(f)
            for entry in data:
                known_names.append(entry["name"])
                known_encodings.append(entry["encoding"])
    except FileNotFoundError:
        print("No face encodings file found. Starting detection-only mode.")  # Fallback to detection without recognition

    cap = cv2.VideoCapture(0)  # Open the default camera (index 0)
    if not cap.isOpened():  # Check if the camera is accessible
        print("Error: Could not open camera.")
        return

    try:
        while True:
            # Capture a single frame from the camera
            ret, frame = cap.read()
            if not ret:  # Handle frame capture errors
                print("Error: Could not read frame.")
                break

            # Convert the frame from BGR to RGB for face_recognition compatibility
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect face locations and encodings in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Process each detected face
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"  # Default to "Unknown" if no match is found

                if True in matches:  # Check if any known face matches the current face
                    match_index = matches.index(True)
                    name = known_names[match_index]  # Get the name of the matched face

                # Draw a bounding box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # Add a label with the person's name
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Display the annotated frame in a window
            cv2.imshow("Face Detection Stream", frame)

            # Exit the loop if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release the camera resource and close the display window
        cap.release()
        cv2.destroyAllWindows()

def camera_stream(mode):
    """
    Dynamically run a camera stream based on the selected mode.
    - Mode 0: Simple camera feed.
    - Mode 1: Face detection feed.

    Args:
        mode (Value): A shared multiprocessing variable indicating the mode.
                      0 = Simple Stream
                      1 = Face Detection Stream
    """
    while True:
        if mode.value == 0:  # Simple camera stream
            simple_camera_feed()
        elif mode.value == 1:  # Face detection stream
            face_detection_feed()
        else:
            print("Invalid mode selected.")  # Handle invalid mode values
            break