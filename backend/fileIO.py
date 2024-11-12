import os

PUBLIC_DIR = "uploads"

os.makedirs(PUBLIC_DIR, exist_ok=True)


def write_to_file(file_records):
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
