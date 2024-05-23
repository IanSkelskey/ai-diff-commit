import sys
from openai_utils import analyze_diff_with_chat_gpt, revise_commit_message
from git_utils import (
    is_in_git_repo,
    has_git_changes,
    get_diff_string,
    get_list_of_changed_files,
    stage_changes,
    commit_changes,
    push_changes,
)
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def confirm_and_commit(diff_string, commit_message):
    print(f"{Fore.CYAN}Generated commit message:\n{commit_message}")
    response = input(f"{Fore.YELLOW}Do you want to commit these changes? (This will stage all changed files and commit the changes.) [y/N] ").lower()
    if response == "y":
        stage_changes()
        commit_changes(commit_message)
        return True
    else:
        revise_commit_message_if_requested(diff_string, commit_message)

def revise_commit_message_if_requested(diff_string, commit_message):
    response = input(f"{Fore.YELLOW}Would you like to provide feedback on the commit message and revise it? [y/N] ").lower()
    if response == "y":
        feedback = input(f"{Fore.YELLOW}Please provide feedback on the commit message: ")
        revised_commit_message = revise_commit_message(diff_string, commit_message, feedback)
        confirm_and_commit(diff_string, revised_commit_message)
    else:
        print(f"{Fore.RED}Changes not committed.")
        return False

def print_changed_files(changed_files):
    print(f"{Fore.GREEN}Changed files:")
    for file in changed_files:
        print(f"{Fore.GREEN}- {file}")

def main():
    auto_push = '-p' in sys.argv or '--push' in sys.argv
    if not is_in_git_repo():
        print(f"{Fore.RED}Error: This program must be run inside a Git repository.")
        return

    if not has_git_changes():
        print(f"{Fore.GREEN}No changes to commit. Your working directory is clean.")
        return

    changed_files = get_list_of_changed_files()
    print_changed_files(changed_files)

    diff_string = get_diff_string()
    if not diff_string:
        print(f"{Fore.RED}No changes detected.")
        return

    commit_message = analyze_diff_with_chat_gpt(diff_string)
    if not commit_message:
        print(f"{Fore.RED}No commit message was generated.")
        return

    if not confirm_and_commit(diff_string, commit_message):
        return

    if auto_push:
        push_changes()
        return

    response = input(f"{Fore.YELLOW}Would you like to push the changes to the remote repository? [y/N] ")
    if response == "y":
        push_changes()
    else:
        print(f"{Fore.YELLOW}Changes not pushed. You can push changes later using 'git push'.")

if __name__ == "__main__":
    main()
