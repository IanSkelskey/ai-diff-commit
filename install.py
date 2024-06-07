import os
import shutil
import subprocess
import sys


# Simple color print functions without dependencies
def print_info(message):
    print(f"\033[96m{message}\033[0m")


def print_warning(message):
    print(f"\033[93m{message}\033[0m")


def print_error(message):
    print(f"\033[91m{message}\033[0m")


def print_success(message):
    print(f"\033[92m{message}\033[0m")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def install_dependencies():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print_success("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies. Error: {e}")
        sys.exit(1)


def set_environment_variable(key, value):
    existing_value = os.environ.get(key)
    if existing_value:
        print_warning(
            f"Environment variable {key} already exists with value: {existing_value}"
        )
        return

    if os.name == "nt":
        os.system(f'setx {key} "{value}"')
    else:
        os.environ[key] = value
        with open(os.path.expanduser("~/.bash_profile"), "a") as bash_profile:
            bash_profile.write(f'\nexport {key}="{value}"\n')
        os.system("source ~/.bash_profile")

    print_success(f"Environment variable {key} set to: {value}")


def on_rm_error(func, path, exc_info):
    import stat

    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def move_repository_contents(source_dir, target_dir):
    if os.path.exists(target_dir):
        print_warning(f"Removing existing directory at {target_dir}")
        shutil.rmtree(target_dir, onerror=on_rm_error)
    os.makedirs(target_dir)
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print_success(f"Repository contents moved to {target_dir}")


def add_to_path(directory):
    path = os.environ.get("PATH", "")
    if directory not in path:
        if os.name == "nt":
            os.system(f'setx PATH "%PATH%;{directory}"')
        else:
            with open(os.path.expanduser("~/.bash_profile"), "a") as bash_profile:
                bash_profile.write(f'\nexport PATH="$PATH:{directory}"\n')
            os.system("source ~/.bash_profile")
        print_success(f"Added {directory} to system PATH.")
    else:
        print_warning(f"{directory} is already in the system PATH.")


def create_batch_file(directory):
    if os.name == "nt":
        batch_content = f"""@echo off
python {directory}\\\\ai_diff_commit\\\\src\\\\ai_diff_commit.py %*
"""
        batch_file_path = os.path.join(directory, "ai_diff_commit.bat")
    else:
        batch_content = f"""#!/bin/bash
python3 {directory}/ai_diff_commit/src/ai_diff_commit.py "$@"
"""
        batch_file_path = os.path.join(directory, "ai_diff_commit.sh")

    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_content)
    os.chmod(batch_file_path, 0o755)
    print_success(f"Script file created at {batch_file_path}")


def main():
    clear_console()
    source_dir = os.getcwd()
    if os.name == "nt":
        scripts_dir = "C:\\Scripts"
        target_dir = "C:\\Scripts\\ai_diff_commit"
    else:
        scripts_dir = os.path.expanduser("~/Scripts")
        target_dir = os.path.join(scripts_dir, "ai_diff_commit")

    print_info("Installing dependencies...")
    install_dependencies()

    if not os.environ.get("OPENAI_API_KEY"):
        api_key = input("Please enter your OpenAI API key: ")
        print_info("Setting environment variable...")
        set_environment_variable("OPENAI_API_KEY", api_key)
    else:
        print_warning("Environment variable OPENAI_API_KEY already exists.")

    print_info("Moving repository contents...")
    move_repository_contents(source_dir, target_dir)

    print_info("Adding to system PATH...")
    add_to_path(scripts_dir)

    print_info("Creating script file...")
    create_batch_file(scripts_dir)

    print_success("Installation completed successfully.")


if __name__ == "__main__":
    main()
