from openai import OpenAI
from constants import SYSTEM_PROMPT

client = OpenAI()


def analyze_diff_with_chat_gpt(diff_string: str):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": diff_string},
            ],
        )
        # Trim the ``` from the start and end of the response
        return completion.choices[0].message.content.strip("`")
    except Exception as e:
        print(f"An error occurred: \n{e}")


def rewrite_commit_message(commit_message: str, feedback: str):
    user_prompt = f"""
    You have generated the following commit message:
    
    ```
    {commit_message}
    ```
    
    Here is some feedback on the commit message:
    
    {feedback}
    
    Please rewrite the commit message based on the feedback.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        # Trim the ``` from the start and end of the response
        return completion.choices[0].message.content.strip("`")
    except Exception as e:
        print(f"An error occurred: \n{e}")
