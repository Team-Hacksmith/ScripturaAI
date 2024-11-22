import os

from flask import Request
from zipfile import ZipFile, ZIP_DEFLATED
import io

PUBLIC_DIR = "uploads"
os.makedirs(PUBLIC_DIR, exist_ok=True)
CLONED_REPO = "cloned_repos"
os.makedirs(CLONED_REPO, exist_ok=True)


def strip_backticks(code):
    if code.startswith("```") and code.endswith("```"):
        code = code[3:]
        first_newline_index = code.find("\n")
        if first_newline_index != -1:
            code = code[first_newline_index + 1 :]

        code = code.rstrip("`")
    return code


def write_files_to_memory(file_records, remove_backticks=True):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w", ZIP_DEFLATED) as zip_file:
        for file_data in file_records:
            filename = file_data.get("filename")
            content = file_data.get("content")

            if remove_backticks:
                content = strip_backticks(content)

            if not filename or not content:
                raise ValueError("Filename or content missing")

            zip_file.writestr(filename, content)

    zip_buffer.seek(0)
    return zip_buffer


def write_files(file_records, remove_backticks=True):
    for file_data in file_records:
        filename = file_data.get("filename")
        content = file_data.get("content")

        if remove_backticks:
            content = strip_backticks(content)

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
        if file_info.filename.startswith(folder_path) and not file_info.is_dir():
            with z.open(file_info) as f:
                filename = file_info.filename
                file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

                try:
                    content = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    content = None

                folder_records.append(
                    {"filename": filename, "fileExt": file_ext, "content": content}
                )

    return folder_records


def read_zip(zip_file):
    file_records = []

    with ZipFile(zip_file) as z:
        for file_info in z.infolist():
            if file_info.is_dir():
                folder_records = read_folder(z, file_info.filename)
                file_records.extend(folder_records)
            else:
                with z.open(file_info) as f:
                    filename = file_info.filename
                    file_ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

                    try:
                        content = f.read().decode("utf-8")
                    except UnicodeDecodeError:
                        content = None

                    file_records.append(
                        {"filename": filename, "fileExt": file_ext, "content": content}
                    )

    return file_records


BLACKLISTED_EXTENSIONS = {
    ".exe",
    ".bin",
    ".dll",
    ".so",
    ".pyc",
    ".class",
    ".pack",
    ".idx",
}
BLACKLISTED_PATHS = {".git"}


def create_file_record(file_path):
    from ai import gen_docstring

    """Creates a dictionary with file information for a given file path, skipping blacklisted files and directories."""

    if any(blacklist in file_path for blacklist in BLACKLISTED_PATHS):
        print(f"Skipping file in blacklisted directory: {file_path}")
        return None

    if os.path.splitext(file_path)[1] in BLACKLISTED_EXTENSIONS:
        print(f"Skipping blacklisted or binary file: {file_path}")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "filename": os.path.basename(file_path),
            "filePath": file_path,
            "content": strip_backticks(gen_docstring(content)),
        }
    except UnicodeDecodeError:
        print(f"Skipping binary or non-UTF-8 file: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def generate_docstring_for_whole_repo(repo_folder_path):
    """Recursively collects all files in a repository folder, modifies them, and writes the new content."""
    file_records = []

    for root, _, files in os.walk(repo_folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_record = create_file_record(file_path)
            if file_record:
                with open(file_record["filePath"], "w", encoding="utf-8") as f:
                    f.write(file_record["content"])

                file_records.append(file_record)

    return file_records


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
