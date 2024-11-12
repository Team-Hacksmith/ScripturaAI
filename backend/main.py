import os
from ai import gen_docstring
from flask import Flask, request
from fileIO import write_to_file

app = Flask(__name__)

PUBLIC_DIR = "uploads"

os.makedirs(PUBLIC_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return "Hello World"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part in the request", 400

    files = request.files.getlist("file")

    file_records = []

    for file in files:
        if not file.filename:
            print("Warning: No file name, skipping file...")
            continue

        filename: str = file.filename
        file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

        content = file.read().decode("utf-8")

        file_info = {"filename": filename, "fileExt": file_ext, "content": content}

        file_records.append(file_info)

    write_to_file(file_records)

    return {"files": file_records}, 200


if __name__ == "__main__":
    app.run(debug=True)
