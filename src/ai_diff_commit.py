"""
AI Diff Commit Script

This script automates the process of generating commit messages using AI.
It can analyze diffs, generate commit messages, and optionally push changes.

Functions:
    parse_arguments: Parses command line arguments.
    initialize_repository: Initializes the repository and clears the console.
    validate_repository: Validates that the script is running inside a Git repository.
    check_for_changes: Checks if there are any changes to commit.
    get_diff_and_selected_files: Gets the diff string and selected files.
    generate_commit_message: Generates a commit message using AI.
    revise_commit_message_if_requested: Revises the commit message if requested.
    confirm_and_commit: Confirms and commits the changes.
    handle_commit_process: Handles the entire commit process.
    main: Main function to run the script.
"""

import sys
import argparse
from ai_utils import analyze_diff_with_chat_gpt, revise_commit_message, set_model
from git_utils import (
    is_in_git_repo,
    has_git_changes,
    get_diff_string_for_file,
    get_diff_string,
    get_list_of_changed_files,
    stage_changes,
    commit_changes,
    push_changes,
    clear_console,
    get_current_branch_name,
)
from prompt_utils import (
    select_changed_files,
    confirm_commit_message,
    request_feedback,
    prompt_push_changes,
    wrap_text,
)
from colors import INFO, WARNING, ERROR, SUCCESS, GIT_INFO, GENERATED
from InquirerPy import prompt


def parse_arguments():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="AI Diff Commit Script")
    parser.add_argument(
        "-p", "--push", action="store_true", help="Automatically push changes."
    )
    parser.add_argument(
        "-a", "--add", action="store_true", help="Automatically add all changes."
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gpt-4o",
        help="Specify the OpenAI API language model.",
    )
    return parser.parse_args()


def initialize_repository():
    """Initializes the repository and clears the console."""
    branch_name = get_current_branch_name()
    clear_console()
    print(wrap_text(f"{GIT_INFO}Current branch: {branch_name}"))
    return branch_name


def validate_repository():
    """Validates that the script is running inside a Git repository."""
    if not is_in_git_repo():
        print(
            wrap_text(
                f"{ERROR}Error: This program must be run inside a Git repository."
            )
        )
        sys.exit(1)


def check_for_changes():
    """Checks if there are any changes to commit."""
    if not has_git_changes():
        print(
            wrap_text(
                f"{SUCCESS}No changes to commit. Your working directory is clean."
            )
        )
        sys.exit(0)


def get_diff_and_selected_files(include_all):
    if include_all:
        diff_string = get_diff_string()
        if not diff_string:
            print(wrap_text(f"{ERROR}No changes detected in the repository."))
            sys.exit(1)
        selected_files = ["."]
    else:
        changed_files = [
            (line[0], line[2:].strip()) for line in get_list_of_changed_files()
        ]
        selected_files = select_changed_files(changed_files)
        if not selected_files:
            print(wrap_text(f"{ERROR}No files selected. Exiting."))
            sys.exit(1)
        diff_string = "\n".join(
            [get_diff_string_for_file(f'"{file}"') for file in selected_files]
        )
        if not diff_string:
            print(wrap_text(f"{ERROR}No changes detected in the selected files."))
            sys.exit(1)
    return diff_string, selected_files


def generate_commit_message(diff_string):
    """Generates a commit message using AI."""
    commit_message = analyze_diff_with_chat_gpt(diff_string)
    if not commit_message:
        print(wrap_text(f"{ERROR}No commit message was generated."))
        sys.exit(1)
    print(wrap_text(f"{GENERATED}Generated commit message:\n{commit_message}\n"))
    return commit_message


def revise_commit_message_if_requested(diff_string, commit_message, selected_files):
    """Revises the commit message if requested."""
    questions = [
        {
            "type": "confirm",
            "message": "Would you like to provide feedback on the commit message and revise it?",
            "name": "revise",
            "default": False,
        }
    ]
    answers = prompt(questions)
    if answers["revise"]:
        feedback = request_feedback()
        revised_commit_message = revise_commit_message(
            diff_string, commit_message, feedback
        )
        print(
            wrap_text(f"{GENERATED}Revised commit message:\n{revised_commit_message}\n")
        )
        return confirm_and_commit(diff_string, revised_commit_message, selected_files)
    else:
        print(f"{ERROR}Changes not committed.")
        return False


def confirm_and_commit(diff_string, commit_message, selected_files):
    """Confirms and commits the changes."""
    if confirm_commit_message(commit_message):
        stage_changes(selected_files)
        commit_changes(commit_message)
        return True
    else:
        return revise_commit_message_if_requested(
            diff_string, commit_message, selected_files
        )


def handle_commit_process(diff_string, selected_files, auto_push):
    """Handles the entire commit process."""
    commit_message = generate_commit_message(diff_string)
    if confirm_and_commit(diff_string, commit_message, selected_files):
        if auto_push:
            push_changes()
        else:
            if prompt_push_changes():
                push_changes()
            else:
                print(
                    wrap_text(
                        f"{WARNING}Changes not pushed. You can push changes later using 'git push'."
                    )
                )


def main():
    """Main function to run the script."""
    args = parse_arguments()
    set_model(args.model)
    initialize_repository()
    validate_repository()
    check_for_changes()
    diff_string, selected_files = get_diff_and_selected_files(args.add)
    handle_commit_process(diff_string, selected_files, args.push)


if __name__ == "__main__":
    main()
