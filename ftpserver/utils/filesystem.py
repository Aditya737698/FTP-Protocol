import os

BASE_DIR = os.path.abspath("server_files/users")  # Jail root

def resolve_path(cwd, path):
    """
    Safely resolve path relative to current working directory.
    Prevents path traversal outside BASE_DIR.
    """
    new_path = os.path.normpath(os.path.join(BASE_DIR, cwd.strip("/"), path))
    if os.path.commonpath([BASE_DIR, new_path]) != BASE_DIR:
        raise ValueError("Access denied: Attempted directory traversal.")
    return new_path

def list_dir(path):
    return os.listdir(path)

def is_directory(path):
    return os.path.isdir(path)

def change_directory(cwd, path):
    resolved = resolve_path(cwd, path)
    if not is_directory(resolved):
        raise NotADirectoryError
    rel = os.path.relpath(resolved, BASE_DIR)
    return "/" if rel == "." else "/" + rel
