import os
from typing import List
from fastapi import UploadFile

UPLOAD_FOLDER = '../uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print(f"handle file uploads, savinf the files and organising them")

def save_uploaded_file(file: UploadFile) -> str:
    """
    Save the uploaded file to the server and return the file path.
    """
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return file_path

def save_multiple_files(files: List[UploadFile]) -> List[str]:
    """
    Save multiple files and return their paths.
    """
    file_paths = []
    for file in files:
        file_path = save_uploaded_file(file)
        file_paths.append(file_path)
    return file_paths
