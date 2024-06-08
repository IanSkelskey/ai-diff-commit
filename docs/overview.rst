Overview
========

AI Diff Commit automates the creation of standardized Git commit messages using OpenAI's API. It ensures adherence to the Conventional Commits specification for clear and meaningful commit history.

Features
--------

- **Automated Commit Messages**: Generate standardized commit messages based on the changes in your repository.
- **Conventional Commits**: Ensure that your commit messages adhere to the Conventional Commits specification.
- **Customizable Commit Messages**: Modify the generated commit message to suit your needs before committing the changes.
- **Automated Git Operations**: Automatically add, commit, and push the changes to your repository.

Limitations
-----------

- **OpenAI API Key**: Requires an API key from OpenAI to access the GPT-3 model for generating commit messages.
- **Internet Connection**: Requires an active internet connection to communicate with the OpenAI API.
- **Always Adds All Changes**: Adds all changes in the repository to the commit, which may not be suitable for all scenarios.
- **Requires a Git Repository**: Needs to be run in a Git repository to access the changes for generating commit messages.
- **Windows Installation**: The installation script is currently designed for Windows systems.
- **Python Version**: Requires Python 3 or higher to run the script.
