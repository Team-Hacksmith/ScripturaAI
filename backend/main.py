import os
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Hello world"


@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if files are present in the request
    if "file" not in request.files:
        return "No file part in the request", 400

    # Get the list of files
    files = request.files.getlist("file")

    # Print each file's name and content
    for file in files:
        print(f"Filename: {file.filename}")
        print("Content:")
        print(
            file.read().decode("utf-8")
        )  # Assuming the file is a text file; adjust for other file types

    return "Files received and printed successfully", 200


if __name__ == "__main__":
    app.run(debug=True)
