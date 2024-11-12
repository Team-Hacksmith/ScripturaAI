import requests
from flask import Blueprint, jsonify, request
import os
import subprocess
from dotenv import load_dotenv
import shutil

load_dotenv()

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CLONE_DIR = "cloned_repos"



def zip_repo(repo_name):
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.isdir(repo_path):
        jsonify({"error": f"Repository {repo_name} does not exist"}), 400

    zip_file_path = shutil.make_archive(repo_path, "zip", repo_path)
    return zip_file_path


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




# def process_repo_files(repo_path):
#     """Processes all the files and folders in the cloned repository."""
#     # Walk through all the files and folders in the cloned repo
#     for root, dirs, files in os.walk(repo_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             # Here, you can process the file, e.g., read, analyze, generate documentation, etc.
#             print(f"Processing file: {file_path}")
#             with open(file_path, "r", encoding="utf-8") as f:
#                 file_content = f.read()
#                 # Perform any processing on the file content here
#                 print(file_content)  # Example: printing the file content

#             # You can call other functions to generate documentation or code comments here
#             # For example, if you want to generate documentation for each file, you can:
#             generate_file_documentation(file, file_content)


# def generate_file_documentation(file_name, file_content):
#     """Generates documentation or comments for a specific file."""
#     print(f"Generating documentation for {file_name}")
#     print(file_name)


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
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Failed to clone the repository: {str(e)}"}), 500
    zip_repo(repo_name)
    delete_repo(repo_name)
    return jsonify(
        {
            "message": f"Repository '{repo_name}' cloned successfully. And zipped successfully",
            "repo": repo_name,
        }
    )
