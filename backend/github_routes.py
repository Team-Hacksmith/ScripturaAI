from flask import jsonify, send_file
import subprocess
import os, subprocess, shutil, yaml
from dotenv import load_dotenv
from fileIO import generate_docstring_for_whole_repo
import io


load_dotenv()

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CLONE_DIR = "cloned_repos"


def zip_repo(repo_name):
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Repository {repo_name} does not exist.")

    # Create the zip file on disk
    zip_file_path = shutil.make_archive(repo_path, "zip", repo_path)

    # Read the zip file into memory
    zip_buffer = io.BytesIO()
    with open(zip_file_path, "rb") as f:
        zip_buffer.write(f.read())

    # Delete the zip file from disk after reading
    os.remove(zip_file_path)

    # Reset buffer position to the beginning
    zip_buffer.seek(0)
    return zip_buffer


def delete_repo(repo_name):
    if not repo_name:
        return jsonify({"error": "Missing 'repo_name' parameter"}), 400

    repo_path = os.path.join(CLONE_DIR, repo_name)

    if not os.path.isdir(repo_path):
        return jsonify({"error": f"Repository '{repo_name}' not found."}), 404

    try:
        shutil.rmtree(repo_path)
        return jsonify({"message": f"Repository '{repo_name}' deleted successfully."})
    except Exception as e:
        return jsonify({"error": f"Failed to delete repository: {str(e)}"}), 500


def clone_repo(repo_url):
    if not repo_url:
        return jsonify({"error": "Missing 'repo_url' parameter"}), 400

    repo_name = repo_url.strip("/").split("/")[-1]
    clone_path = os.path.join(CLONE_DIR, repo_name)

    if os.path.isdir(clone_path):
        return jsonify({"error": f"Repository {repo_name} already cloned."}), 400

    try:
        print(f"Cloning repository: git clone {repo_url} {clone_path}")
        subprocess.check_call(["git", "clone", repo_url, clone_path])
        git_dir = os.path.join(clone_path, ".git")
        if os.path.isdir(git_dir):
            shutil.rmtree(git_dir)  # Remove the .git folder
            print(f"Deleted .git folder in {clone_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Failed to clone the repository: {str(e)}"}), 500

    generate_docstring_for_whole_repo(os.path.join(CLONE_DIR, repo_name))
    # Zip the repository into an in-memory buffer
    zip_buffer = zip_repo(repo_name)

    # Send the zip file as a downloadable response
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=f"{repo_name}.zip",
        mimetype="application/zip",
    )


def generate_mkdocs_yml(site_name, docs_dir="docs"):
    # Set up the base structure for mkdocs.yml
    mkdocs_config = {"site_name": site_name, "docs_dir": docs_dir, "nav": []}

    # Traverse the docs directory to populate navigation
    for root, _, files in os.walk(docs_dir):
        rel_path = os.path.relpath(root, docs_dir)

        if rel_path == ".":
            # Root level files
            for file in files:
                if file.endswith(".md"):
                    page_name = os.path.splitext(file)[0].capitalize()
                    mkdocs_config["nav"].append({page_name: file})
        else:
            # Subdirectories and nested files
            section = {"name": os.path.basename(root).capitalize(), "items": []}
            for file in files:
                if file.endswith(".md"):
                    page_name = os.path.splitext(file)[0].capitalize()
                    section["items"].append({page_name: os.path.join(rel_path, file)})

            if section["items"]:
                mkdocs_config["nav"].append(
                    {os.path.basename(root).capitalize(): section["items"]}
                )

    # Save the mkdocs.yml file
    with open("mkdocs.yml", "w") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False)
    print("mkdocs.yml generated with auto-indexed files.")