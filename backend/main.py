import os
from flask import Flask, request
from fileIO import write_to_file
app = Flask(__name__)

app = Flask(__name__)

# Define the public directory to save files
PUBLIC_DIR = 'public'

# Ensure the public directory exists
os.makedirs(PUBLIC_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if files are present in the request
    if "file" not in request.files:
        return "No file part in the request", 400

    # Get the list of files
    files = request.files.getlist("file")

    # Initialize a list to store file details
    file_records = []

    # Process each file
    for file in files:
        # Extract the filename and file extension
        filename = file.filename
        file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

        # Read file content and decode it (assuming it's a text file)
        content = file.read().decode("utf-8")  # Adjust decoding if dealing with non-text files

        # Create a dictionary for the current file
        file_info = {"filename": filename, "fileExt": file_ext, "content": content}

        # Add the file info dictionary to the list
        file_records.append(file_info)

    # Call the function to save the files in the public folder
    write_to_file(file_records)

    # Return the list of file records as a JSON response
    return {"files": file_records}, 200



if __name__ == "__main__":
    app.run(debug=True)
