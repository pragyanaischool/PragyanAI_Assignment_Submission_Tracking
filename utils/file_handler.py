# utils/file_handler.py

import os
from config.settings import UPLOAD_DIR


def save_file(file, usn, test_id):
    if file is None:
        return None

    folder = f"{UPLOAD_DIR}/{usn}/{test_id}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{file.name}"

    with open(path, "wb") as f:
        f.write(file.read())

    return path


def delete_file(file_path):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
