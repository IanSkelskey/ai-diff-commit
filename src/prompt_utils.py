from InquirerPy import prompt
from colors import INFO, WARNING, ERROR, SUCCESS

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

def confirm_commit_message(commit_message):
    print(f"{INFO}Generated commit message:\n{commit_message}")
    response = input(f"{WARNING}Do you want to commit these changes? (This will stage all selected files and commit the changes.) [y/N] ").lower()
    return response == "y"

def request_feedback():
    return input(f"{WARNING}Please provide feedback on the commit message: ")

def prompt_push_changes():
    response = input(f"{WARNING}Would you like to push the changes to the remote repository? [y/N] ")
    return response == "y"
