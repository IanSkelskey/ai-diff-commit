import sys
from openai_utils import analyze_diff_with_chat_gpt, revise_commit_message
from git_utils import (
    is_in_git_repo,
    has_git_changes,
    get_diff_string_for_file,
    get_list_of_changed_files,
    stage_changes,
    commit_changes,
    push_changes,
)
from colorama import init, Fore, Style
from InquirerPy import prompt

# Initialize colorama
init(autoreset=True)

STATUS_DESCRIPTIONS = {
    "A": "Addition",
    "C": "Copy",
    "D": "Deletion",
    "M": "Modification",
    "R": "Renaming",
    "T": "Type change",
    "U": "Unmerged",
    "X": "Unknown"
}

def confirm_and_commit(diff_string, commit_message, auto_push=False):
    print(f"{Fore.CYAN}Generated commit message:\n{commit_message}")
    response = input(f"{Fore.YELLOW}Do you want to commit these changes? (This will stage all selected files and commit the changes.) [y/N] ").lower()
    if response == "y":
        stage_changes()
        commit_changes(commit_message)
        if auto_push:
            push_changes()
        return True
    else:
        revise_commit_message_if_requested(diff_string, commit_message, auto_push)

def revise_commit_message_if_requested(diff_string, commit_message, auto_push=False):
    response = input(f"{Fore.YELLOW}Would you like to provide feedback on the commit message and revise it? [y/N] ").lower()
    if response == "y":
        feedback = input(f"{Fore.YELLOW}Please provide feedback on the commit message: ")
        revised_commit_message = revise_commit_message(diff_string, commit_message, feedback)
        confirm_and_commit(diff_string, revised_commit_message, auto_push)
    else:
        print(f"{Fore.RED}Changes not committed.")
        return False

def select_changed_files(changed_files):
    choices = [
        {"name": f"{STATUS_DESCRIPTIONS.get(status, 'Unknown')} - {filename}", "value": filename}
        for status, filename in changed_files
    ]
    questions = [
        {
            "type": "checkbox",
            "message": "Select files to include in the commit:",
            "name": "files",
            "choices": choices,
        }
    ]
    answers = prompt(questions)
    return answers["files"]

def main():
    auto_push = '-p' in sys.argv or '--push' in sys.argv
    if not is_in_git_repo():
        print(f"{Fore.RED}Error: This program must be run inside a Git repository.")
        return

    if not has_git_changes():
        print(f"{Fore.GREEN}No changes to commit. Your working directory is clean.")
        return

    changed_files = parse_changed_files(get_list_of_changed_files())
    selected_files = select_changed_files(changed_files)
    
    if not selected_files:
        print(f"{Fore.RED}No files selected. Exiting.")
        return
    
    diff_string = get_diff_string_for_files(selected_files)
    if not diff_string:
        print(f"{Fore.RED}No changes detected in the selected files.")
        return

    commit_message = analyze_diff_with_chat_gpt(diff_string)
    if not commit_message:
        print(f"{Fore.RED}No commit message was generated.")
        return

    if not confirm_and_commit(diff_string, commit_message, auto_push):
        return

    if auto_push:
        push_changes()
    else:
        response = input(f"{Fore.YELLOW}Would you like to push the changes to the remote repository? [y/N] ")
        if response == "y":
            push_changes()
        else:
            print(f"{Fore.YELLOW}Changes not pushed. You can push changes later using 'git push'.")

def parse_changed_files(changed_files):
    parsed_files = []
    for line in changed_files:
        status = line[0]
        filename = line[2:].strip()  # Remove the status and the space
        parsed_files.append((status, filename))
    return parsed_files

def get_diff_string_for_files(files):
    # Generate diff string for selected files
    diffs = []
    for file in files:
        diff = get_diff_string_for_file(file)
        if diff:
            diffs.append(diff)
    return "\n".join(diffs)

if __name__ == "__main__":
    main()
