import os
from fileIO import read_files, strip_backticks, write_files
from ai import gen_docstring, gen_algorithm
from flask import Flask, request, jsonify

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
    gen_type = request_data.get("type")

    if (not gen_type) or (gen_type not in ["code", "algo", "guide", "diagram"]):
        raise ValueError("Invalid type")

    result = ""

    match gen_type:
        case "code":
            result = gen_docstring(request_data.get("content"))
        case "algo":
            result = gen_algorithm(request_data.get("content"))
        case "guide":
            result = gen_algorithm(request_data.get("content"))
        case "diagram":
            result = "Not implemented yet"
        case _:
            raise ValueError("Invalid type")

    return {"content": strip_backticks(result), "type": gen_type}


if __name__ == "__main__":
    app.run(debug=True)
