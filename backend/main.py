import os
from fileIO import read_files, strip_backticks, write_files_to_memory
from flask import Flask, request, jsonify, send_file
from ai import gen_docstring, gen_algorithm, gen_mermaid, gen_guide
from github_routes import clone_repo


app = Flask(__name__)

PUBLIC_DIR = "uploads"

os.makedirs(PUBLIC_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return "Hello World"


@app.route("/upload", methods=["POST"])
def upload_file():
    file_records = read_files(request)
    gen_type = request.form.get("type")

    if (not gen_type) or (gen_type not in ["code", "algo", "guide", "diagram"]):
        raise ValueError("Invalid type")

    output_file_records = []

    for file_data in file_records:
        filename = file_data.get("filename", None)
        content = file_data.get("content", None)
        fileExt = file_data.get("fileExt", None)

        if not filename or not content or not fileExt:
            raise ValueError("Invalid data")

        result = ""

        match gen_type:
            case "code":
                result = gen_docstring(content)
            case "algo":
                result = gen_algorithm(content)
                filename = filename.rsplit(".", 1)[0] + ".md"
            case "guide":
                result = gen_guide(content)
                filename = filename.rsplit(".", 1)[0] + ".md"
            case "diagram":
                result = gen_mermaid(content)
                filename = filename.rsplit(".", 1)[0] + ".mmd"
            case _:
                raise ValueError("Invalid type")

        output_file_records.append(
            {
                "filename": filename,
                "fileExt": fileExt,
                "content": result,
            }
        )

    # Get the in-memory zip file containing all files
    zip_buffer = write_files_to_memory(output_file_records)

    # Send the zip file as a downloadable response
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name="files.zip",
    )


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
            result = gen_guide(request_data.get("content"))
        case "diagram":
            result = gen_mermaid(request_data.get("content"))
        case _:
            raise ValueError("Invalid type")

    return {"content": strip_backticks(result), "type": gen_type}


@app.route("/cloneRepo", methods=["POST"])
def cloneRepo():
    repo_url = request.json.get("url")

    if not repo_url:
        return jsonify({"error": "Missing url parameter"}), 400

    # Call the clone_repo function to clone the repo
    return clone_repo(repo_url)


if __name__ == "__main__":
    app.run(debug=True)
