import subprocess
import os

def is_in_git_repo():
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

def has_git_changes():
    status_output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
    return len(status_output.strip()) > 0

def get_list_of_changed_files():
    status_output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
    return [line for line in status_output.strip().split('\n') if line]

def get_diff_string_for_file(file_path):
    return subprocess.run(["git", "diff", file_path], capture_output=True, text=True).stdout

def get_diff_string():
    return subprocess.run(["git", "diff"], capture_output=True, text=True).stdout

def stage_changes(file_path="."):
    subprocess.run(["git", "add", file_path])
    print("Changes staged successfully.")

def commit_changes(commit_message):
    subprocess.run(["git", "commit", "-m", commit_message])
    print("Changes committed successfully.")

def push_changes():
    subprocess.run(["git", "push"])
    print("Changes pushed successfully.")
