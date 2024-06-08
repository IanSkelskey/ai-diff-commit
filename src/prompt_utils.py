"""
Prompt Utilities

This module provides utility functions for interacting with the user through prompts.

Functions:
    get_api_key: Prompts the user to enter their OpenAI API key.
    select_changed_files: Prompts the user to select the changed files to include in the commit.
    confirm_commit_message: Prompts the user to confirm the commit message.
    request_feedback: Prompts the user to provide feedback on the commit message.
    prompt_push_changes: Prompts the user to push the changes to the remote repository.
    wrap_text: Wraps text to the specified width.
"""

from InquirerPy import prompt
import textwrap

def get_api_key():
    """Prompts the user to enter their OpenAI API key."""
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
    """Prompts the user to select the changed files to include in the commit."""
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
    """Prompts the user to confirm the commit message."""
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
    """Prompts the user to provide feedback on the commit message."""
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
    """Prompts the user to push the changes to the remote repository."""
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

def wrap_text(text, width=120):
    """Wraps text to the specified width."""
    paragraphs = text.split("\n")
    wrapped_paragraphs = [textwrap.fill(p, width) for p in paragraphs]
    return "\n".join(wrapped_paragraphs)
