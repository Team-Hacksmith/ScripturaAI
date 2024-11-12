import os

from flask import Request

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


def read_files(request: Request):
    if "file" not in request.files:
        return "No file part in the request", 400

    files = request.files.getlist("file")
    file_records = []

    for file in files:
        if not file.filename:
            print("Warning: No file name, skipping file...")
            continue

        filename: str = file.filename
        file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

        content = file.read().decode("utf-8")

        file_info = {"filename": filename, "fileExt": file_ext, "content": content}

        file_records.append(file_info)

    return file_records
