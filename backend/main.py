import os
from fileIO import read_files, strip_backticks, write_files_to_memory
from flask import Flask, request, jsonify, send_file
from ai import gen_docstring, gen_algorithm, gen_mermaid, gen_guide, gen_markdown
from github_routes import clone_repo
import subprocess

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
