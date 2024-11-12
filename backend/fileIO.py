import os

from flask import Request

PUBLIC_DIR = "uploads"

os.makedirs(PUBLIC_DIR, exist_ok=True)


def strip_backticks(code):
    # Check if the code starts and ends with backticks
    if code.startswith("```") and code.endswith("```"):
        # Remove the opening backticks and language identifier
        code = code[3:]  # Remove '```' from the start

        # Find the index of the first newline after the language identifier
        first_newline_index = code.find("\n")

        # If a newline exists after the language identifier, remove the first line
        if first_newline_index != -1:
            # Skip the first line and keep the rest of the code
            code = code[first_newline_index + 1 :]

        # Remove any trailing backticks (```) from the end
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
