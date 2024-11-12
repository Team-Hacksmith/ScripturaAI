import os

from flask import Request

from zipfile import ZipFile
from typing import List, Any

PUBLIC_DIR = "uploads"

os.makedirs(PUBLIC_DIR, exist_ok=True)


def strip_backticks(code):
    if code.startswith("```") and code.endswith("```"):
        code = code[3:]  
        first_newline_index = code.find("\n")
        if first_newline_index != -1:
            code = code[first_newline_index + 1 :]
            
        code = code.rstrip("`")
    return code



def write_files(file_records):
    for file_data in file_records:
        filename = file_data.get("filename")
        content = file_data.get("content")

        if not filename or not content:
            raise ValueError("Filename or content missing")

        file_path = os.path.join(PUBLIC_DIR, filename)

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w") as file:
                file.write(content)

        except Exception as e:
            raise Exception(f"An error occurred while saving the file: {str(e)}")


def file_to_record(file):
    if not file or not file.filename:
        print("Warning: No file name, skipping file...")
        return

    filename: str = file.filename
    file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

    content = file.read().decode("utf-8")

    file_info = {"filename": filename, "fileExt": file_ext, "content": content}

    return file_info


def read_files(request: Request):
    if "file" not in request.files:
        return "No file part in the request", 400

    file_records = []

    files = request.files.getlist("file")

    for file in files:
        if not file.filename:
            print("Warning: No file name, skipping file...")
            continue
        filename: str = file.filename
        file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
        if file_ext == "zip":
            zip_file_records = read_zip(file)
            file_records.extend(zip_file_records)
            continue

        file_records.append(file_to_record(file))

    return file_records


def read_folder(z, folder_path):
    """Reads all files inside a folder in a ZIP archive."""
    folder_records = []

    for file_info in z.infolist():
        # Check if file is within the current folder path and is not a directory
        if file_info.filename.startswith(folder_path) and not file_info.is_dir():
            with z.open(file_info) as f:
                filename = file_info.filename
                file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

                try:
                    # Decode the content to UTF-8 if possible
                    content = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    # Handle binary or non-UTF-8 files
                    content = None

                # Append file information to folder records
                folder_records.append(
                    {"filename": filename, "fileExt": file_ext, "content": content}
                )

    return folder_records


def read_zip(zip_file):
    file_records = []

    with ZipFile(zip_file) as z:
        for file_info in z.infolist():
            # If it's a directory, read its contents
            if file_info.is_dir():
                folder_records = read_folder(z, file_info.filename)
                file_records.extend(folder_records)
            else:
                # If it's a file, read it directly
                with z.open(file_info) as f:
                    filename = file_info.filename
                    file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

                    try:
                        # Decode the content to UTF-8 if possible
                        content = f.read().decode("utf-8")
                    except UnicodeDecodeError:
                        # Handle binary or non-UTF-8 files
                        content = None

                    file_records.append(
                        {"filename": filename, "fileExt": file_ext, "content": content}
                    )

    return file_records
