import sys
from ai_utils import analyze_diff_with_chat_gpt, revise_commit_message
from git_utils import (
    is_in_git_repo,
    has_git_changes,
    get_diff_string_for_file,
    get_diff_string,
    get_list_of_changed_files,
    stage_changes,
    commit_changes,
    push_changes,
)
from prompt_utils import select_changed_files, confirm_commit_message, request_feedback, prompt_push_changes
from colors import INFO, WARNING, ERROR, SUCCESS

def confirm_and_commit(diff_string, commit_message, auto_push=False):
    if confirm_commit_message(commit_message):
        stage_changes()
        commit_changes(commit_message)
        if auto_push:
            push_changes()
        return True
    else:
        revise_commit_message_if_requested(diff_string, commit_message, auto_push)

def revise_commit_message_if_requested(diff_string, commit_message, auto_push=False):
    if input(f"{WARNING}Would you like to provide feedback on the commit message and revise it? [y/N] ").lower() == "y":
        feedback = request_feedback()
        revised_commit_message = revise_commit_message(diff_string, commit_message, feedback)
        confirm_and_commit(diff_string, revised_commit_message, auto_push)
    else:
        print(f"{ERROR}Changes not committed.")
        return False

def main():
    auto_push = '-p' in sys.argv or '--push' in sys.argv
    include_all = '-a' in sys.argv or '--all' in sys.argv

    if not is_in_git_repo():
        print(f"{ERROR}Error: This program must be run inside a Git repository.")
        return

    if not has_git_changes():
        print(f"{SUCCESS}No changes to commit. Your working directory is clean.")
        return

    if include_all:
        diff_string = get_diff_string()
        if not diff_string:
            print(f"{ERROR}No changes detected in the repository.")
            return
    else:
        changed_files = [(line[0], line[2:].strip()) for line in get_list_of_changed_files()]
        selected_files = select_changed_files(changed_files)
        
        if not selected_files:
            print(f"{ERROR}No files selected. Exiting.")
            return
        
        diff_string = "\n".join([get_diff_string_for_file(file) for file in selected_files])
        if not diff_string:
            print(f"{ERROR}No changes detected in the selected files.")
            return

    commit_message = analyze_diff_with_chat_gpt(diff_string)
    if not commit_message:
        print(f"{ERROR}No commit message was generated.")
        return

    if not confirm_and_commit(diff_string, commit_message, auto_push):
        return

    if auto_push:
        push_changes()
    else:
        if prompt_push_changes():
            push_changes()
        else:
            print(f"{WARNING}Changes not pushed. You can push changes later using 'git push'.")

if __name__ == "__main__":
    main()
