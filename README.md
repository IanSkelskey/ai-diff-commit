# AI Diff Commit

Automates the creation of standardized Git commit messages using [OpenAI's API](https://platform.openai.com/docs/), ensuring adherence to the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for clear and meaningful commit history.

## Features

- **Automated Commit Messages**: Generate standardized commit messages based on the changes in your repository.
- **Conventional Commits**: Ensure that your commit messages adhere to the Conventional Commits specification.
- **Customizable Commit Messages**: Modify the generated commit message to suit your needs before committing the changes.
- **Automated Git Operations**: Automatically add, commit, and push the changes to your repository.

## Limitations

- **OpenAI API Key**: Requires an API key from OpenAI to access the GPT-3 model for generating commit messages.
- **Internet Connection**: Requires an active internet connection to communicate with the OpenAI API.
- **Always Adds All Changes**: Adds all changes in the repository to the commit, which may not be suitable for all scenarios.
- **Requires a Git Repository**: Needs to be run in a Git repository to access the changes for generating commit messages.

## Usage Instructions (Windows)

I have only tested this on Windows, but it should work on other operating systems with minor modifications. For now, I will provide instructions for setting up the script on Windows that worked for me.

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies using the following command:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your OpenAI API key by creating a `.env` file in the project directory and adding the following line:
    ```plaintext
    OPENAI_API_KEY=<YOUR_API_KEY>
    ```
4. Move the repository contents to wherever to store scripts. I used `C:\Scripts` for this example.
5. Add the path to the `C:\Scripts` directory to your system's PATH environment variable.
6. Create a `ai_diff_commit.bat` file in the `C:\Scripts` directory with the following content:
    ```batch
    @echo off
    python C:\Scripts\ai_diff_commit\src\ai_diff_commit.py %*
    ```
7. Now you can run the `ai_diff_commit` command from any directory to generate commit messages based on the changes in your repository.