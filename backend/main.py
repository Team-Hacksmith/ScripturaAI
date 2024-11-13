import os
from ai import gen_docstring, gen_algorithm, gen_mermaid, gen_guide, gen_markdown
from flask import Flask, request, jsonify
from fileIO import read_files, write_files
from github_routes import clone_repo, generate_mkdocs_yml
import yaml, subprocess
import shutil

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
        return jsonify({"content": text}), 200
    else:
        return jsonify({"error": "No text data provided"}), 400


@app.route("/genMermaid", methods=["POST"])
def generate_mermaid():
    data = request.get_json()
    if data and "text" in data:
        text = data["text"]
        res = gen_mermaid(text)
        # write_files(res)
        return jsonify({"content": res}), 200

    else:
        return jsonify({"error": "No text data provided"}), 400


@app.route("/genGuide", methods=["POST"])
def generate_guide():
    data = request.get_json()
    if data and "text" in data:
        text = data["text"]
        gen_guide(text)
        # write_files({"filename": "userGuide.md", "content": res}, False)
        return jsonify({"content": text}), 200
    else:
        return jsonify({"error": "No text data provided"}), 400


@app.route("/single", methods=["POST"])
def single():
    request_data = request.get_json()

    return {"content": gen_docstring(request_data.get("content"))}


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
    repo_url = request.json.get("repo_url")

    if not repo_url:
        return jsonify({"error": "Missing repo_url parameter"}), 400

    # Call the clone_repo function to clone the repo
    return clone_repo(repo_url)


import os
import subprocess
from flask import jsonify


@app.route("/generateWebsite", methods=["POST"])
def generateWebsite():
    data = request.get_json()

    # Check if required parameters are provided in the request body
    if not data or "site_name" not in data or "repo_url" not in data:
        return jsonify({"error": "Missing 'site_name' or 'repo_url' in request"}), 400

    site_name = data["site_name"]
    repo_url = data["repo_url"]

    # Extract repo_name from repo_url (assuming URL ends with .git)
    repo_name = os.path.splitext(os.path.basename(repo_url))[0]

    # Create the site_name directory first
    if not os.path.exists(site_name):
        os.makedirs(site_name)  # Create site_name directory if it doesn't exist

    # Create the mkdocs.yml file inside site_name directory
    mkdocs_yml_path = os.path.join(site_name, "mkdocs.yml")
    with open(mkdocs_yml_path, "w") as yml_file:
        yml_file.write(f"site_name: {site_name}\n")
        yml_file.write(f"docs_dir: docs\n")  # We'll create the docs folder next

        # Append theme configuration to mkdocs.yml
        yml_file.write("theme:\n")
        yml_file.write("  name: material\n")  # Adding the Material theme

    # Create the docs folder inside site_name directory
    mkdocs_dir = os.path.join(site_name, "docs")
    os.makedirs(mkdocs_dir, exist_ok=True)  # Create docs folder if it doesn't exist

    # Define the path for the cloned repo
    cloned_repo_path = os.path.join("cloned_repos", repo_name)

    # Clone repository if it doesn't exist in cloned_repos
    if not os.path.exists(cloned_repo_path):
        os.makedirs("cloned_repos", exist_ok=True)  # Ensure parent directory exists
        clone_cmd = f"git clone {repo_url} {cloned_repo_path}"
        subprocess.run(clone_cmd, shell=True, check=True)

    # Define blacklisted extensions
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

    # Traverse cloned repo, process files, and save markdown files in docs directory
    for dirpath, _, filenames in os.walk(cloned_repo_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_ext = os.path.splitext(filename)[1]

            # Skip files with blacklisted extensions
            if file_ext in blacklisted_extensions:
                print(f"Skipping {filename} due to blacklisted extension.")
                continue

            # Read the file content and generate markdown
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Generate markdown using gen_markdown
                processed_content = gen_markdown(content)

                # Save markdown if processed_content is generated successfully
                if processed_content:
                    markdown_filename = os.path.join(
                        mkdocs_dir, f"{os.path.splitext(filename)[0]}.md"
                    )
                    with open(markdown_filename, "w", encoding="utf-8") as md_file:
                        md_file.write(processed_content)
                    print(f"Saved {markdown_filename}")
                else:
                    print(f"Failed to process {filename} or file is blacklisted.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Run mkdocs build command in the site_name directory
    try:
        subprocess.run(
            "mkdocs serve --dev-addr=0.0.0.0:8001",
            shell=True,
            check=True,
            cwd=site_name,
        )

        print("MkDocs build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during mkdocs build: {e}")

    return (
        jsonify({"success": f"Website created with markdown files in {mkdocs_dir}"}),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
