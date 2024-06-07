import subprocess
import os
import mimetypes
from colors import INFO, ERROR, SUCCESS

# Constants for Git commands and options
GIT_COMMAND = "git"
GIT_STATUS = ["status", "--porcelain"]
GIT_DIFF = ["diff"]
GIT_ADD = ["add"]
GIT_COMMIT = ["commit", "-m"]
GIT_PUSH = ["push"]
GIT_CURRENT_BRANCH = ["rev-parse", "--abbrev-ref", "HEAD"]
GIT_INSIDE_WORK_TREE = ["rev-parse", "--is-inside-work-tree"]
GIT_LS_FILES = ["ls-files", "--error-unmatch"]

# Constants for subprocess options
DEVNULL = subprocess.DEVNULL
TEXT = True
CAPTURE_OUTPUT = True

def is_in_git_repo():
    try:
        subprocess.run([GIT_COMMAND] + GIT_INSIDE_WORK_TREE, check=True, stdout=DEVNULL, stderr=DEVNULL, text=TEXT)
        return True
    except subprocess.CalledProcessError:
        return False

def has_git_changes():
    status_output = subprocess.run([GIT_COMMAND] + GIT_STATUS, capture_output=CAPTURE_OUTPUT, text=TEXT).stdout
    return len(status_output.strip()) > 0

def get_current_branch_name():
    return subprocess.run([GIT_COMMAND] + GIT_CURRENT_BRANCH, capture_output=CAPTURE_OUTPUT, text=TEXT).stdout.strip()

def get_list_of_changed_files():
    status_output = subprocess.run([GIT_COMMAND] + GIT_STATUS, capture_output=CAPTURE_OUTPUT, text=TEXT).stdout
    changed_files = [line for line in status_output.strip().split('\n') if line]

    new_files = []
    for line in changed_files:
        status = line[0]
        filename = line[3:].strip() if status == '?' else line[2:].strip()
        if filename.endswith('/'):
            files_in_directory = subprocess.run([GIT_COMMAND, "ls-files", "--others", "--exclude-standard", filename], capture_output=CAPTURE_OUTPUT, text=TEXT).stdout
            for file in files_in_directory.strip().split('\n'):
                new_files.append(f"{status} {file}")
        else:
            new_files.append(line)

    return new_files

def is_binary_file(file_path):
    print(f"{INFO}Checking if {file_path} is a binary file.")
    mime_type, _ = mimetypes.guess_type(file_path)
    print(f"{INFO}Mime type: {mime_type}")
    return mime_type is not None and mime_type.startswith('image')

def get_diff_string_for_file(file_path):
    if is_binary_file(file_path):
        return f"Binary file detected: {file_path} - Skipping diff."

    if subprocess.run([GIT_COMMAND] + GIT_LS_FILES + [file_path], stdout=DEVNULL, stderr=DEVNULL, text=TEXT).returncode != 0:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return f"Untracked file: {file_path}\n{content}"
        except FileNotFoundError:
            return f"{ERROR}Untracked file: {file_path}\nFile not found."
        except UnicodeDecodeError:
            return f"{ERROR}Untracked file: {file_path}\nBinary file detected - Skipping diff."
    else:
        try:
            return subprocess.run([GIT_COMMAND] + GIT_DIFF + [file_path], capture_output=CAPTURE_OUTPUT, text=TEXT, encoding='utf-8').stdout
        except UnicodeDecodeError:
            return f"{ERROR}Tracked file: {file_path}\nBinary file detected - Skipping diff."

def get_diff_string():
    return subprocess.run([GIT_COMMAND] + GIT_DIFF, capture_output=CAPTURE_OUTPUT, text=TEXT, encoding='utf-8').stdout

def stage_changes(selected_files=["."]):
    for file_path in selected_files:
        subprocess.run([GIT_COMMAND] + GIT_ADD + [file_path], stdout=DEVNULL, stderr=DEVNULL)
    print(f"{SUCCESS}Changes staged successfully.")

def commit_changes(commit_message):
    subprocess.run([GIT_COMMAND] + GIT_COMMIT + [commit_message], stdout=DEVNULL, stderr=DEVNULL)
    print(f"{SUCCESS}Changes committed successfully.")

def push_changes():
    subprocess.run([GIT_COMMAND] + GIT_PUSH, stdout=DEVNULL, stderr=DEVNULL)
    print(f"{SUCCESS}Changes pushed successfully.")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
