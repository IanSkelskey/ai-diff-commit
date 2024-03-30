import subprocess
import os


def is_in_git_repo():
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def has_git_changes():
    status_output = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    ).stdout
    return len(status_output.strip()) > 0


def get_diff_string():
    combined_diffs = [
        get_unstaged_diff(),
        get_staged_diff(),
    ] + get_untracked_diffs()
    return "\n".join(combined_diffs)


def get_unstaged_diff():
    return subprocess.run(["git", "diff"], capture_output=True, text=True).stdout


def get_staged_diff():
    return subprocess.run(
        ["git", "diff", "--cached"], capture_output=True, text=True
    ).stdout


def get_untracked_diffs():
    untracked_files_command = ["git", "ls-files", "--others", "--exclude-standard"]
    untracked_files_output = subprocess.run(
        untracked_files_command, capture_output=True, text=True
    ).stdout
    untracked_files = [file for file in untracked_files_output.split("\n") if file]

    diffs = []
    for file in untracked_files:
        if not is_git_ignored(file):
            diffs.append(generate_diff_for_untracked_file(file))
    return diffs


def is_git_ignored(file_path):
    result = subprocess.run(["git", "check-ignore", file_path], capture_output=True)
    return result.returncode == 0


def generate_diff_for_untracked_file(file_path):
    if os.path.isfile(file_path):  # Make sure it's a file, not a directory
        return subprocess.run(
            ["git", "diff", "--no-index", "--", "/dev/null", file_path],
            capture_output=True,
            text=True,
        ).stdout
    return ""
