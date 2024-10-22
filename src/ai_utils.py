"""
AI Utilities

This module provides utility functions for interacting with the OpenAI API
to generate and revise commit messages based on diffs.

Functions:
    set_model: Sets the model for the OpenAI API.
    analyze_diff_with_chat_gpt: Analyzes the diff and generates a commit message.
    revise_commit_message: Revises the commit message based on user feedback.
"""

import os
import time
from openai import OpenAI
from colors import AI_INFO, ERROR

# Determine the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
system_prompt_path = os.path.join(script_dir, "..", "lib", "prompts", "conventional_long.md")

client = OpenAI()

MODEL = "gpt-4o"

def set_model(model_name: str):
    """Sets the model for the OpenAI API."""
    global MODEL
    MODEL = model_name

with open(system_prompt_path, "r") as file:
    SYSTEM_PROMPT = file.read()

def _get_response(message: str):
    """Gets the response from the OpenAI API."""
    max_retries = 5
    backoff_factor = 2
    retry_count = 0

    while retry_count < max_retries:
        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
            )
            print(f"{AI_INFO}Generating commit message...")
            print(f"{AI_INFO}Language Model: {completion.model}")
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                retry_count += 1
                wait_time = backoff_factor ** retry_count
                print(f"{ERROR}Rate limit error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"{ERROR}An error occurred: \n{e}")
                break
    return None

def analyze_diff_with_chat_gpt(diff_string: str):
    """Analyzes the diff and generates a commit message."""
    return _get_response(diff_string).strip("`")

def revise_commit_message(diff_string: str, commit_message: str, feedback: str):
    """Revises the commit message based on user feedback."""
    user_prompt = f"""
    You have generated the following commit message:
    
    ```
    {commit_message}
    ```
    
    Based on the following diff:
        
    ``` 
    {diff_string}
    ```
    
    Here is some feedback on the commit message:
    
    {feedback}
    
    Please rewrite the commit message based on the feedback.
    """
    return _get_response(user_prompt).strip("`")
