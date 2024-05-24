from InquirerPy import prompt

def get_api_key():
    questions = [
        {
            "type": "input",
            "message": "Please enter your OpenAI API key:",
            "name": "api_key",
        }
    ]
    answers = prompt(questions)
    return answers["api_key"]

def select_changed_files(changed_files):
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
    questions = [
        {
            "type": "confirm",
            "message": "Do you want to commit these changes?",
            "name": "commit",
            "default": False,
        }
    ]
    answers = prompt(questions)
    return answers["commit"]

def request_feedback():
    questions = [
        {
            "type": "input",
            "message": "Please provide feedback on the commit message:",
            "name": "feedback",
        }
    ]
    answers = prompt(questions)
    return answers["feedback"]

def prompt_push_changes():
    questions = [
        {
            "type": "confirm",
            "message": "Would you like to push the changes to the remote repository?",
            "name": "push",
            "default": False,
        }
    ]
    answers = prompt(questions)
    return answers["push"]
