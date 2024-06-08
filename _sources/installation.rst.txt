Installation Instructions
=========================

.. image:: https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white
.. image:: https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white

To set up the script, follow these steps:

1. Clone the repository and navigate to the project directory.
2. Run the installation script using the following command:
    ```bash
    python install.py
    ```

	**Note:** You may need to specify `python3` instead of `python` depending on your system configuration.

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

	**Note:** If the command `ai_diff_commit` is still not found, please restart your terminal or run `source ~/.zshrc` or `source ~/.bash_profile` manually.
