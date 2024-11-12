# file_utils.py
import os

# Define the public directory to save files
PUBLIC_DIR = 'public'

# Ensure the public directory exists
os.makedirs(PUBLIC_DIR, exist_ok=True)

def write_to_file(file_records):
    for file_data in file_records:
        # Extract the filename and content from the file data
        filename = file_data.get("filename")
        content = file_data.get("content")

        if not filename or not content:
            raise ValueError("Filename or content missing")

        # Define the full path for the file in the public directory
        file_path = os.path.join(PUBLIC_DIR, filename)

        try:
            # Ensure subdirectories in filename path are created
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write content to the file in the public directory
            with open(file_path, "w") as file:
                file.write(content)

        except Exception as e:
            raise Exception(f"An error occurred while saving the file: {str(e)}")
