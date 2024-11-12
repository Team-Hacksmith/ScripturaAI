import os
from ai import gen_docstring, gen_algorithm
from flask import Flask, request, jsonify
from fileIO import read_files, write_files
from github_routes import clone_repo

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Hello World"


PUBLIC_DIR = "uploads"
os.makedirs(PUBLIC_DIR, exist_ok=True)


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


@app.route("/genalgo", methods=["POST"])
def generate_algorithm():
    data = request.get_json()
    if data and "text" in data:
        text = data["text"]
        gen_algorithm(text)
        return jsonify({"received_text": text}), 200

    else:
        return jsonify({"error": "No text data provided"}), 400


@app.route("/single", methods=["POST"])
def single():
    request_data = request.get_json()

    return {"content": gen_docstring(request_data.get("content"))}


@app.route("/cloneRepo", methods=["POST"])
def cloneRepo():
    repo_url = request.json.get("repo_url")

    if not repo_url:
        return jsonify({"error": "Missing repo_url parameter"}), 400

    # Call the clone_repo function to clone the repo
    return clone_repo(repo_url)


if __name__ == "__main__":
    app.run(debug=True)
