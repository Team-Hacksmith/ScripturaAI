import os
import threading

from fileIO import read_files, strip_backticks, write_files_to_memory
from flask import Flask, request, jsonify, send_file
from ai import gen_docstring, gen_algorithm, gen_mermaid, gen_guide, gen_markdown
from github_routes import clone_repo
import subprocess
from flask_cors import CORS
import shutil

app = Flask(__name__)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"

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


@app.route("/genMarkdown", methods=["POST"])
def genMarkdown():
    data = request.get_json()
    if data and "text" in data:
        text = data["text"]
        gen_markdown(text)
        return jsonify({"content": text}), 200
    else:
        return jsonify({"error": "No text data provided"}), 400


@app.route("/cloneRepo", methods=["POST"])
def cloneRepo():
    repo_url = request.json.get("url")

    if not repo_url:
        return jsonify({"error": "Missing url parameter"}), 400

    return clone_repo(repo_url)


import os
import subprocess
from flask import jsonify

mkdocs_processes = {}  # Dictionary to store active processes by site name


def run_mkdocs_serve(site_name, port):
    process = subprocess.Popen(
        f"mkdocs serve --dev-addr=0.0.0.0:{port}", shell=True, cwd=site_name
    )
    mkdocs_processes[site_name] = process


def cleanup_site(site_name):
    # Terminate mkdocs serve process if it's running
    process = mkdocs_processes.get(site_name)
    if process and process.poll() is None:  # Check if process is still running
        process.terminate()  # Gracefully terminate the process
        process.wait()  # Wait for termination to complete
        print(f"Terminated mkdocs serve for {site_name}")


@app.route("/generateWebsite", methods=["POST"])
def generateWebsite():
    data = request.get_json()

    if not data or "site_name" not in data or "repo_url" not in data:
        return jsonify({"error": "Missing 'site_name' or 'repo_url' in request"}), 400

    site_name = data["site_name"]
    repo_url = data["repo_url"]
    port = data["port"]

    repo_name = os.path.splitext(os.path.basename(repo_url))[0]

    if not os.path.exists(site_name):
        os.makedirs(site_name)

    mkdocs_yml_path = os.path.join(site_name, "mkdocs.yml")
    with open(mkdocs_yml_path, "w") as yml_file:
        yml_file.write(f"site_name: {site_name}\n")
        yml_file.write(f"docs_dir: docs\n")
        yml_file.write("theme:\n")
        yml_file.write("  name: material\n")

    mkdocs_dir = os.path.join(site_name, "docs")
    os.makedirs(mkdocs_dir, exist_ok=True)

    cloned_repo_path = os.path.join("cloned_repos", repo_name)

    git_dir = os.path.join(cloned_repo_path, ".git")
    if not os.path.exists(cloned_repo_path):
        os.makedirs("cloned_repos", exist_ok=True)
        clone_cmd = f"git clone {repo_url} {cloned_repo_path}"
        subprocess.run(clone_cmd, shell=True, check=True)

    if os.path.isdir(git_dir):
        print(f"Deleting .git folder in {cloned_repo_path}")
        shutil.rmtree(git_dir)
        print(f"Deleted .git folder in {cloned_repo_path}")
    else:
        print(f".git folder not found in {cloned_repo_path}, skipping deletion.")

    blacklisted_extensions = {
        ".exe",
        ".dll",
        ".bin",
        ".out",
        ".md",
        ".zip",
        ".pack",
        ".idk",
        ".rev",
    }

    for dirpath, _, filenames in os.walk(cloned_repo_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1]

            if file_ext in blacklisted_extensions:
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                processed_content = gen_markdown(content)
                if processed_content:
                    markdown_filename = os.path.join(
                        mkdocs_dir, f"{os.path.splitext(filename)[0]}.md"
                    )
                    with open(markdown_filename, "w", encoding="utf-8") as md_file:
                        md_file.write(processed_content)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Start mkdocs serve in a new thread
    thread = threading.Thread(target=run_mkdocs_serve, args=(site_name, port))
    thread.start()

    return (
        jsonify(
            {
                "url": f"http://localhost:{port}",
                "success": f"Website created with markdown files in {mkdocs_dir}",
            }
        ),
        200,
    )


@app.route("/stopServer", methods=["POST"])
def stop_server():
    data = request.get_json()
    site_name = data.get("site_name")

    if site_name and site_name in mkdocs_processes:
        cleanup_site(site_name)
        return (
            jsonify({"success": f"Server for {site_name} stopped and cleaned up."}),
            200,
        )
    else:
        return jsonify({"error": "Site not found or already stopped."}), 404


if __name__ == "__main__":
    app.run(debug=True)
