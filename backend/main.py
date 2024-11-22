import os
import threading

from fileIO import (
    handle_remove_error,
    read_files,
    strip_backticks,
    write_files_to_memory,
)
from flask import Flask, request, jsonify, send_file, send_from_directory
from ai import gen_docstring, gen_algorithm, gen_mermaid, gen_guide, gen_markdown
from github_routes import clone_repo
import subprocess
from flask_cors import CORS
import shutil

app = Flask(__name__, static_folder="mkdocs_output")
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
    print(repo_url)

    if not repo_url:
        return jsonify({"error": "Missing url parameter"}), 400

    return clone_repo(repo_url)


import os
import subprocess
from flask import jsonify

mkdocs_processes = {}  # Dictionary to store active processes by site name


def run_mkdocs_serve(site_name, port):
    process = subprocess.Popen(
        f"mkdocs serve --dev-addr=0.0.0.0:{port}",
        shell=True,
        cwd=os.path.join("mkdocs_output", site_name),
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
def generate_website():
    data = request.get_json()

    if not data or "site_name" not in data or "repo_url" not in data:
        return jsonify({"error": "Missing 'site_name' or 'repo_url' in request"}), 400

    site_name = data["site_name"].strip().replace(" ", "_")
    repo_url = data["repo_url"]

    # Define paths
    mkdocs_config_dir = os.path.join("mkdocs_output", site_name)
    cloned_repo_path = os.path.join("cloned_repos", site_name)

    # Prepare directories
    if not os.path.exists(mkdocs_config_dir):
        os.makedirs(mkdocs_config_dir)

    # Create the mkdocs.yml file with the correct site_dir
    mkdocs_yml_path = os.path.join(mkdocs_config_dir, "mkdocs.yml")
    with open(mkdocs_yml_path, "w") as yml_file:
        yml_file.write(f"site_name: {site_name}\n")
        yml_file.write(f"docs_dir: docs\n")
        yml_file.write(f"site_dir: site\n")
        yml_file.write("theme:\n")
        yml_file.write("  name: material\n")

    docs_dir = os.path.join(mkdocs_config_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    # Clone repository
    if not os.path.exists(cloned_repo_path):
        os.makedirs("cloned_repos", exist_ok=True)
        subprocess.run(
            f"git clone {repo_url} {cloned_repo_path}", shell=True, check=True
        )
        # Delete the .git folder
        git_dir = os.path.join(cloned_repo_path, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir, onexc=handle_remove_error)
            print(f"Deleted .git folder in {cloned_repo_path}")

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

    home_page_content = f"""
    # {site_name}

    Welcome to {site_name}
    """

    with open(os.path.join(docs_dir, "index.md"), "w", encoding="utf-8") as home_file:
        home_file.write(home_page_content)

    for dirpath, dirnames, filenames in os.walk(cloned_repo_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1]

            if file_ext == ".md":
                shutil.copy(
                    os.path.join(dirpath, filename), os.path.join(docs_dir, filename)
                )
                continue

            if file_ext in blacklisted_extensions:
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                print(f"Processing: {filename}")
                processed_content = gen_markdown(content)
                print(f"Processed: {filename}")
                if processed_content:
                    markdown_filename = os.path.join(
                        docs_dir, f"{os.path.splitext(filename)[0]}.md"
                    )
                    with open(markdown_filename, "w", encoding="utf-8") as md_file:
                        md_file.write(processed_content)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("Processed all files. Now building mkdocs...")

    # Build the MkDocs site
    subprocess.run(f"mkdocs build -f {mkdocs_yml_path}", shell=True, check=True)

    site_output_dir = f"mkdocs_output/{site_name}/site"

    return (
        jsonify(
            {
                "success": f"Website built successfully at {site_output_dir}",
                "url": f"http://localhost:5000/static/{site_name}/site/index.html",
            }
        ),
        200,
    )


@app.route("/static/<site_name>/site/", defaults={"path": ""})
@app.route("/static/<site_name>/site/<path:path>")
def serve_site(site_name, path):
    """Serve the built MkDocs site files."""
    site_root = os.path.join("mkdocs_output", site_name, "site")

    # If no specific file is provided, serve index.html
    if path == "":
        path = "index.html"
    else:
        # If the path is a directory, serve index.html from that directory
        potential_index = os.path.join(site_root, path, "index.html")
        if os.path.isdir(os.path.join(site_root, path)) and os.path.exists(
            potential_index
        ):
            path = os.path.join(path, "index.html")

    # Serve the file
    try:
        return send_from_directory(site_root, path)
    except FileNotFoundError:
        return "File not found", 404


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
