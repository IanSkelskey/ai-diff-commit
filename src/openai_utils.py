from openai import OpenAI
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

client = OpenAI()

with open("lib/system_prompt.md", "r") as file:
    SYSTEM_PROMPT = file.read()

def _get_response(message: str):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
        )
        print(f"{Fore.CYAN}Model: {completion.model}")
        return completion.choices[0].message.content
    except Exception as e:
        print(f"{Fore.RED}An error occurred: \n{e}")

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
