import os
import time
from openai import OpenAI
from colors import AI_INFO, ERROR

# Determine the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
system_prompt_path = os.path.join(script_dir, "..", "lib", "system_prompt.md")

client = OpenAI()

MODEL = "gpt-4o"

def set_model(model_name: str):
    global MODEL
    MODEL = model_name

with open(system_prompt_path, "r") as file:
    SYSTEM_PROMPT = file.read()


def _get_response(message: str):
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
    return _get_response(diff_string).strip("`")

def revise_commit_message(diff_string: str, commit_message: str, feedback: str):
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
