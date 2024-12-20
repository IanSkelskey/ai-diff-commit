# AI Diff Commit

![Version](https://img.shields.io/badge/version-0.0.3-blue)

Automates the creation of standardized Git commit messages using [OpenAI's API](https://platform.openai.com/docs/).

![JavaScript](https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/typescript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-00A79D?style=for-the-badge&logo=openai&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![npm](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)

## Built-In Commit Standards

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-FB607C?style=for-the-badge&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iQ2FwYV8xIiBkYXRhLW5hbWU9IkNhcGEgMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCA4MDAgODAwIj4KICA8ZGVmcz4KICAgIDxzdHlsZT4KICAgICAgLmNscy0xIHsKICAgICAgICBmaWxsOiAjZmZmOwogICAgICAgIHN0cm9rZTogI2ZmZjsKICAgICAgICBzdHJva2UtbWl0ZXJsaW1pdDogNS40OwogICAgICAgIHN0cm9rZS13aWR0aDogMS4zcHg7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxnIGlkPSJTVkdSZXBvX2ljb25DYXJyaWVyIiBkYXRhLW5hbWU9IlNWR1JlcG8gaWNvbkNhcnJpZXIiPgogICAgPGc+CiAgICAgIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTY4MC4zLDExOS44Yy0zNi40LTM2LjQtNzguOC02NC45LTEyNi04NC45QzUwNS40LDE0LjIsNDUzLjUsMy43LDQwMCwzLjdzLTEwNS40LDEwLjUtMTU0LjMsMzEuMmMtNDcuMiwyMC04OS42LDQ4LjUtMTI2LDg0LjktMzYuNCwzNi40LTY0LjksNzguOC04NC45LDEyNkMxNC4yLDI5NC42LDMuNywzNDYuNSwzLjcsNDAwczEwLjUsMTA1LjQsMzEuMiwxNTQuM2MyMCw0Ny4yLDQ4LjUsODkuNiw4NC45LDEyNiwzNi40LDM2LjQsNzguOCw2NC45LDEyNiw4NC45LDQ4LjksMjAuNywxMDAuOCwzMS4yLDE1NC4zLDMxLjJzMTA1LjQtMTAuNSwxNTQuMy0zMS4yYzQ3LjItMjAsODkuNi00OC41LDEyNi04NC45LDM2LjQtMzYuNCw2NC45LTc4LjgsODQuOS0xMjYsMjAuNy00OC45LDMxLjItMTAwLjgsMzEuMi0xNTQuM3MtMTAuNS0xMDUuNC0zMS4yLTE1NC4zYy0yMC00Ny4yLTQ4LjUtODkuNi04NC45LTEyNlpNNDAwLDY3NC41Yy0xNTEuNiwwLTI3NC41LTEyMi45LTI3NC41LTI3NC41UzI0OC40LDEyNS41LDQwMCwxMjUuNXMyNzQuNSwxMjIuOSwyNzQuNSwyNzQuNS0xMjIuOSwyNzQuNS0yNzQuNSwyNzQuNVoiLz4KICAgICAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJNNDAwLDc5N2MtNTMuNiwwLTEwNS42LTEwLjUtMTU0LjUtMzEuMi00Ny4zLTIwLTg5LjctNDguNi0xMjYuMi04NS4xLTM2LjQtMzYuNC02NS4xLTc4LjktODUuMS0xMjYuMkMxMy41LDUwNS42LDMsNDUzLjYsMyw0MDBzMTAuNS0xMDUuNiwzMS4yLTE1NC41YzIwLTQ3LjMsNDguNi04OS43LDg1LjEtMTI2LjIsMzYuNC0zNi40LDc4LjktNjUuMSwxMjYuMi04NS4xQzI5NC40LDEzLjUsMzQ2LjQsMyw0MDAsM3MxMDUuNiwxMC41LDE1NC41LDMxLjJjNDcuMywyMCw4OS43LDQ4LjYsMTI2LjIsODUuMSwzNi40LDM2LjQsNjUuMSw3OC45LDg1LjEsMTI2LjIsMjAuNyw0OSwzMS4yLDEwMSwzMS4yLDE1NC41cy0xMC41LDEwNS42LTMxLjIsMTU0LjVjLTIwLDQ3LjMtNDguNiw4OS43LTg1LjEsMTI2LjItMzYuNCwzNi40LTc4LjksNjUuMS0xMjYuMiw4NS4xLTQ5LDIwLjctMTAxLDMxLjItMTU0LjUsMzEuMlpNNDAwLDQuM2MtNTMuNCwwLTEwNS4yLDEwLjUtMTU0LDMxLjEtNDcuMSwxOS45LTg5LjQsNDguNS0xMjUuNyw4NC44LTM2LjMsMzYuMy02NC44LDc4LjYtODQuOCwxMjUuNy0yMC42LDQ4LjgtMzEuMSwxMDAuNi0zMS4xLDE1NHMxMC41LDEwNS4yLDMxLjEsMTU0YzE5LjksNDcuMSw0OC41LDg5LjQsODQuOCwxMjUuNywzNi4zLDM2LjMsNzguNiw2NC44LDEyNS43LDg0LjgsNDguOCwyMC42LDEwMC42LDMxLjEsMTU0LDMxLjFzMTA1LjItMTAuNSwxNTQtMzEuMWM0Ny4xLTE5LjksODkuNC00OC41LDEyNS43LTg0LjgsMzYuMy0zNi4zLDY0LjgtNzguNiw4NC44LTEyNS43LDIwLjYtNDguOCwzMS4xLTEwMC42LDMxLjEtMTU0cy0xMC41LTEwNS4yLTMxLjEtMTU0Yy0xOS45LTQ3LjEtNDguNS04OS40LTg0LjgtMTI1LjctMzYuMy0zNi4zLTc4LjYtNjQuOC0xMjUuNy04NC44LTQ4LjgtMjAuNi0xMDAuNi0zMS4xLTE1NC0zMS4xWk00MDAsNjc1Yy03My41LDAtMTQyLjUtMjguNi0xOTQuNS04MC41LTUxLjktNTEuOS04MC41LTEyMS04MC41LTE5NC41czI4LjYtMTQyLjUsODAuNS0xOTQuNWM1MS45LTUxLjksMTIxLTgwLjUsMTk0LjUtODAuNXMxNDIuNSwyOC42LDE5NC41LDgwLjVjNTEuOSw1MS45LDgwLjUsMTIxLDgwLjUsMTk0LjVzLTI4LjYsMTQyLjUtODAuNSwxOTQuNWMtNTEuOSw1MS45LTEyMSw4MC41LTE5NC41LDgwLjVaTTQwMCwxMjYuMWMtNzMuMiwwLTE0MiwyOC41LTE5My43LDgwLjItNTEuNyw1MS43LTgwLjIsMTIwLjUtODAuMiwxOTMuN3MyOC41LDE0Miw4MC4yLDE5My43YzUxLjcsNTEuNywxMjAuNSw4MC4yLDE5My43LDgwLjJzMTQyLTI4LjUsMTkzLjctODAuMmM1MS43LTUxLjcsODAuMi0xMjAuNSw4MC4yLTE5My43cy0yOC41LTE0Mi04MC4yLTE5My43Yy01MS43LTUxLjctMTIwLjUtODAuMi0xOTMuNy04MC4yWiIvPgogICAgPC9nPgogIDwvZz4KPC9zdmc+)](https://www.conventionalcommits.org/en/v1.0.0/)
[![Evergreen ILS](https://img.shields.io/badge/Evergreen%20ILS-379676?style=for-the-badge&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0NjguMjQgNDg0LjM5Ij4KICA8ZGVmcz4KICAgIDxzdHlsZT4KICAgICAgLmNscy0xIHsKICAgICAgICBmaWxsOiAjZmZmOwogICAgICB9CiAgICA8L3N0eWxlPgogIDwvZGVmcz4KICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0xNzkuMTUsNDg0LjM5di00MS4zOWMtNTIuNzgtMy40OS0xMDUuNTEtMTAuMjEtMTU3LjI4LTIwLjktNi4yOS0xLjMtMTMuNDctMi41Ni0xOS41NS00LjM4LS43My0uMjItMi40LS4yNC0yLjMxLTEuMjNsMTAzLjQ3LTcxLjQ4LTY0LjY3LTE0Ljg3LDg2LjY1LTcyLjQ1LTQ3LjE5LTE0Ljg3LDczLjA2LTc2LjMyLTM0LjI0LTE0Ljg3TDIzNC4zOCwwbDExNi43NywxNTEuNjQtMzQuMjQsMTQuODcsNzMuMDYsNzYuMzItNDcuMTksMTQuODcsODYuNjUsNzIuNDUtNjQuNjcsMTQuODcsMTAzLjQ3LDcxLjQ4Yy4wOS45OS0xLjU4LDEuMDEtMi4zMSwxLjIzLTYsMS44LTEzLjMyLDMuMDktMTkuNTUsNC4zOC01MS43NiwxMC43MS0xMDQuNTEsMTcuMzEtMTU3LjI4LDIwLjl2NDEuMzlzLTEwOS45NCwwLTEwOS45NCwwWiIvPgo8L3N2Zz4=)](https://evergreen-ils.org/)

## Features

-   **Automated Commit Messages**: Generate standardized commit messages based on the changes in your repository.
-   **Automated Git Operations**: Automatically add, commit, and push the changes to your repository.

## Limitations

-   **OpenAI API Key**: Requires an API key from OpenAI to access the GPT-3 model for generating commit messages.
-   **Internet Connection**: Requires an active internet connection to communicate with the OpenAI API.
-   **Requires a Git Repository**: Needs to be run in a Git repository to access the changes for generating commit messages.

## Installation Instructions

Commit Generator can be installed globally using npm:

```bash
npm install -g ai-diff-commit
```

## Usage Instructions

Once you have set up the script using the installation instructions, you can use the `ai-diff-commit` command to generate commit messages based on the changes in your repository.

### Flags

-   `-a`, `--all`: Add all changes in the repository to the commit. By default, only the modified files are added.
-   `-h`, `--help`: Display help information for the script.
-   `-m`, `--model`: Specify the OpenAI API language model to use for generating commit messages. See the [OpenAI API documentation](https://platform.openai.com/docs/models/) for available models.
-   `-p`, `--push`: Automatically push the changes to the remote repository after committing.
    -   If a remote branch is not specified, the changes are pushed to a new remote branch with the same name as the current branch. (I plan to make this more configurable in the future.)

For example, to generate a commit message based on all changes in the repository and push the changes to the remote repository, you can use the following command:

```bash
ai-diff-commit -a -p
```

## Bug Reports and Feature Requests

If you encounter any issues while using the script or have ideas for new features, please [open an issue on GitHub](https://github.com/IanSkelskey/ai-diff-commit/issues/new).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
