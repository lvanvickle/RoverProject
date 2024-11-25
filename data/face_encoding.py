import face_recognition
import os
import json

def get_face_encodings(folder_path, output_format="json"):
    """
    Scans the folder for images, computes face encodings, and saves them along with names.
    Args:
        folder_path (str): Path to the folder containing images.
        output_format (str): The desired output format ('json' or 'csv').
    """
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    encodings_data = []

    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in valid_extensions):  # Check valid extensions
            img_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(img_path)  # Load the image
            encodings = face_recognition.face_encodings(image)  # Compute face encodings

            if encodings:  # Ensure at least one face is detected
                clean_name = filename.split(".")[0].replace("_", " ").title()  # Extract and clean the name
                encodings_data.append({"name": clean_name, "encoding": encodings[0].tolist()})  # Convert to list

    # Save to the desired format
    if output_format.lower() == "json":
        save_to_json(encodings_data)
    elif output_format.lower() == "csv":
        save_to_csv(encodings_data)
    else:
        print(f"Unsupported format: {output_format}. Please choose 'json' or 'csv'.")

def save_to_json(data):
    """Saves encoding data to a JSON file."""
    with open("face_encodings.json", "w") as f:
        json.dump(data, f, indent=4)  # Dump JSON-serializable data
    print("Encodings saved to 'face_encodings.json'.")

def save_to_csv(data):
    """Saves encoding data to a CSV file."""
    import csv
    with open("face_encodings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["Name", "Encoding"])
        # Write rows
        for entry in data:
            writer.writerow([entry["name"], entry["encoding"]])
    print("Encodings saved to 'face_encodings.csv'.")

if __name__ == "__main__":
    # Path to the folder containing images
    folder_path = "./sample_faces"

    # Choose the output format (either 'json' or 'csv')
    output_format = "json"  # Change to "csv" if you prefer CSV

    # Generate and save encodings
    get_face_encodings(folder_path, output_format)
