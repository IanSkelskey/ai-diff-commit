from git_utils import is_in_git_repo, has_git_changes, get_diff_string
from openai_utils import analyze_diff_with_chat_gpt, revise_commit_message
import subprocess

def confirm_and_commit(diff_string, commit_message):
    print(f"Generated commit message:\n{commit_message}")
    response = input(
        "Do you want to commit these changes? (This will stage all changed files as well as commit and push the changes.) [y/N] "
    ).lower()
    if response == "y":
        stage_command = ["git", "add", "."]
        commit_command = ["git", "commit", "-m", commit_message]
        push_command = ["git", "push"]
        subprocess.run(stage_command)
        subprocess.run(commit_command)
        subprocess.run(push_command)
        print("Changes committed and pushed successfully.")
    else:
        ## If the user doesn't want to commit, ask for feedback and revise the commit message
        response = input("Would you like to provide feedback on the commit message and revise it?").lower()
        
        if response == "y":
            feedback = input("Please provide feedback on the commit message: ")
            revised_commit_message = revise_commit_message(diff_string, commit_message, feedback)
            confirm_and_commit(diff_string, revised_commit_message)
        else:
            print("Changes not committed.")
        


def main():
    if not is_in_git_repo():
        print("Error: This program must be run inside a Git repository.")
        return

    if not has_git_changes():
        print("No changes to commit. Your working directory is clean.")
        return

    diff_string = get_diff_string()
    if not diff_string:
        print("No changes detected.")
        return

    commit_message = analyze_diff_with_chat_gpt(diff_string)
    if not commit_message:
        print("No commit message was generated.")
        return

    confirm_and_commit(diff_string, commit_message)


if __name__ == "__main__":
    main()
