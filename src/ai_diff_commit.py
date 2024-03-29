import os
import subprocess
import sys
from openai import OpenAI
from constants import SYSTEM_PROMPT

client = OpenAI()


def analyze_diff_with_chat_gpt():
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_diff_string()},
            ],
        )
        # Trim the ``` from the start and end of the response
        return completion.choices[0].message.content.strip("`")
    except Exception as e:
        print(f"An error occurred: \n{e}")
        sys.exit(1)


def get_diff_string():
    unstaged_diff_output = get_unstaged_diff()
    staged_diff_output = get_staged_diff()
    untracked_diffs = get_untracked_diffs()
    combined_diff = "\n".join(
        [unstaged_diff_output, staged_diff_output] + untracked_diffs
    )
    return combined_diff


def get_unstaged_diff():
    unstaged_diff_command = ["git", "diff"]
    unstaged_diff_output = subprocess.run(
        unstaged_diff_command, capture_output=True, text=True
    ).stdout
    return unstaged_diff_output


def get_staged_diff():
    staged_diff_command = ["git", "diff", "--cached"]
    staged_diff_output = subprocess.run(
        staged_diff_command, capture_output=True, text=True
    ).stdout
    return staged_diff_output


def get_untracked_diffs():
    untracked_files_and_dirs = get_untracked_files_and_dirs()
    untracked_diffs = []
    for path in untracked_files_and_dirs:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not is_git_ignored(file_path):
                        diff_output = generate_diff_for_untracked_file(file_path)
                        if diff_output:  # Only add if not empty
                            untracked_diffs.append(diff_output)
        else:
            diff_output = generate_diff_for_untracked_file(path)
            if diff_output:  # Only add if not empty
                untracked_diffs.append(diff_output)
    return untracked_diffs


def get_untracked_files_and_dirs():
    # This command lists untracked files, respecting .gitignore
    untracked_files_command = ["git", "ls-files", "--others", "--exclude-standard"]
    untracked_files_output = subprocess.run(
        untracked_files_command, capture_output=True, text=True
    ).stdout
    # Files are listed line by line
    untracked_files_and_dirs = untracked_files_output.split("\n")
    # Filter out empty strings in case there are any
    return [file for file in untracked_files_and_dirs if file]


def is_git_ignored(file_path):
    """Check if a file is ignored by git."""
    result = subprocess.run(["git", "check-ignore", file_path], capture_output=True)
    return result.returncode == 0


def generate_diff_for_untracked_file(file_path):
    """Generate a diff for an untracked file if it's not ignored."""
    if not is_git_ignored(file_path):
        untracked_diff_command = [
            "git",
            "diff",
            "--no-index",
            "--",
            "/dev/null",
            file_path,
        ]
        return subprocess.run(
            untracked_diff_command, capture_output=True, text=True
        ).stdout
    return ""


def confirm_and_commit(commit_message):
    print(f"Generated commit message:\n{commit_message}")
    response = input("Do you want to commit these changes? (This will stage all changed files as well as commit and push the changes.) [y/N] ").lower()
    if response == "y":
        stage_command = ["git", "add", "."]
        commit_command = ["git", "commit", "-m", commit_message]
        push_command = ["git", "push"]
        subprocess.run(stage_command)
        subprocess.run(commit_command)
        subprocess.run(push_command)
        print("Changes committed and pushed successfully.")
    else:
        ## If the user doesn't want to commit, offer to generate a new commit message
        response = input("Do you want to generate a new commit message? [y/N] ").lower()
        if response == "y":
            main()
        else:
            print("Exiting without committing changes.")


def main():
    commit_message = analyze_diff_with_chat_gpt()
    confirm_and_commit(commit_message)


if __name__ == "__main__":
    main()
