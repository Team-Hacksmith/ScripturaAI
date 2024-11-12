import os
from ai import gen_docstring
from flask import Flask, request
from fileIO import read_files, strip_backticks, write_files

app = Flask(__name__)

PUBLIC_DIR = "uploads"

os.makedirs(PUBLIC_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return "Hello World"


@app.route("/upload", methods=["POST"])
def upload_file():
    file_records = read_files(request)
    output_file_records = []

    for file_data in file_records:
        filename = file_data.get("filename", None)
        content = file_data.get("content", None)
        fileExt = file_data.get("fileExt", None)

        if not filename or not content or not fileExt:
            raise ValueError("Invalid data")

        output_file_records.append(
            {
                "filename": filename,
                "fileExt": fileExt,
                "content": gen_docstring(content),
            }
        )

    write_files(output_file_records)

    return {"files": output_file_records}, 200


@app.route("/single", methods=["POST"])
def single():
    request_data = request.get_json()

    return {"content": strip_backticks(gen_docstring(request_data.get("content")))}


if __name__ == "__main__":
    app.run(debug=True)
