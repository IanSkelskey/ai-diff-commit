import subprocess

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
    changed_files = [line for line in status_output.strip().split('\n') if line]

    new_files = []
    for line in changed_files:
        status = line[0]
        filename = line[3:].strip() if status == '?' else line[2:].strip()
        if filename.endswith('/'):
            files_in_directory = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", filename], capture_output=True, text=True).stdout
            for file in files_in_directory.strip().split('\n'):
                new_files.append(f"{status} {file}")
        else:
            new_files.append(line)

    return new_files

def get_diff_string_for_file(file_path):
    if subprocess.run(["git", "ls-files", "--error-unmatch", file_path], capture_output=True, text=True).returncode != 0:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return f"Untracked file: {file_path}\n{content}"
        except FileNotFoundError:
            return f"Untracked file: {file_path}\nFile not found."
    else:
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
