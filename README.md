<img src="lib/logo.svg" width="100">

# AI Diff Commit

Automates the creation of standardized Git commit messages using [OpenAI's API](https://platform.openai.com/docs/), ensuring adherence to the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for clear and meaningful commit history.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenAI](https://img.shields.io/badge/OpenAI-00A79D?style=for-the-badge&logo=openai&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

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
- **Windows Installation**: The installation script is currently designed for Windows systems.
- **Python Version**: Requires Python 3 or higher to run the script.

## Dependencies

- [**Colorama**](https://pypi.org/project/colorama/): For colored output in the terminal.
- [**OpenAI**](https://pypi.org/project/openai/): For interacting with the OpenAI API.
- [**InquirerPy**](https://pypi.org/project/InquirerPy/): For interactive command-line user interfaces.

## Installation Instructions

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)

To set up the script, follow these steps:

1. Clone the repository and navigate to the project directory.
2. Run the installation script using the following command: 
    ```bash
    python install.py
    ```
    > **Note:** You may need to specify `python3` instead of `python` depending on your system configuration.

This script will:
- Install the required dependencies.
- Prompt you to enter your OpenAI API key and set it as an environment variable.
- Move the repository contents to:
  - `C:\\Scripts\\ai_diff_commit` for Windows
  - `~/Scripts/ai_diff_commit` for macOS
- Add the `Scripts` directory to your system's PATH environment variable.
- Create a script file in the `Scripts` directory to run the script from any location:
  - `ai_diff_commit.bat` for Windows
  - `ai_diff_commit.sh` for macOS
- For macOS, it will automatically source the appropriate shell configuration file to apply changes immediately if using zsh.

> **Note:** If the command `ai_diff_commit` is still not found, please restart your terminal or run `source ~/.zshrc` or `source ~/.bash_profile` manually.

## Usage Instructions

Once you have set up the script using the installation instructions, you can use the `ai_diff_commit` command to generate commit messages based on the changes in your repository.

### Flags

- `-a`, `--all`: Add all changes in the repository to the commit. By default, only the modified files are added.
- `-h`, `--help`: Display help information for the script.
- `-m`, `--model`: Specify the OpenAI API language model to use for generating commit messages.
- `-p`, `--push`: Automatically push the changes to the remote repository after committing.

For example, to generate a commit message based on all changes in the repository and push the changes to the remote repository, you can use the following command:

```bash
ai_diff_commit -a -p
```

## File Selection

The script will prompt you to select the files you want to include in the commit. You can use the arrow keys to navigate the list and the spacebar to select or deselect files. Press `Enter` to proceed with the selected files.

![File Selection Screenshot](lib/screenshots/file_selection.png)

## Example Output

![Sample Output](lib/screenshots/output.png)