import os
import shutil
import subprocess
import sys
from src.colors import INFO, WARNING, ERROR, SUCCESS
from src.prompt_utils import get_api_key

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{SUCCESS}Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print(f"{ERROR}Failed to install dependencies.")
        sys.exit(1)

def set_environment_variable(key, value):
    existing_value = os.environ.get(key)
    if existing_value:
        print(f"{WARNING}Environment variable {key} already exists with value: {existing_value}")
        return
    os.system(f'setx {key} "{value}"')
    print(f"{SUCCESS}Environment variable {key} set to: {value}")

def on_rm_error(func, path, exc_info):
    """Error handler for `shutil.rmtree`.

    If the error is due to an access error (read-only file), it attempts to add write permission and then retries.
    If the error is for another reason, it re-raises the error.
    """
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def move_repository_contents(source_dir, target_dir):
    if os.path.exists(target_dir):
        print(f"{WARNING}Removing existing directory at {target_dir}")
        shutil.rmtree(target_dir, onerror=on_rm_error)
    os.makedirs(target_dir)
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print(f"{SUCCESS}Repository contents moved to {target_dir}")

def add_to_path(directory):
    path = os.environ.get("PATH", "")
    if directory not in path:
        os.system(f'setx PATH "%PATH%;{directory}"')
        print(f"{SUCCESS}Added {directory} to system PATH.")
    else:
        print(f"{WARNING}{directory} is already in the system PATH.")

def create_batch_file(directory):
    batch_content = f"""@echo off
python {directory}\\ai_diff_commit\\src\\ai_diff_commit.py %*
"""
    batch_file_path = os.path.join(directory, "ai_diff_commit.bat")
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_content)
    print(f"{SUCCESS}Batch file created at {batch_file_path}")

def main():
    clear_console()
    source_dir = os.getcwd()
    scripts_dir = "C:\\Scripts"
    target_dir = "C:\\Scripts\\ai_diff_commit"

    print(f"{INFO}Installing dependencies...")
    install_dependencies()

    if not os.environ.get("OPENAI_API_KEY"):
        api_key = get_api_key()
        print(f"{INFO}Setting environment variable...")
        set_environment_variable("OPENAI_API_KEY", api_key)
    else:
        print(f"{WARNING}Environment variable OPENAI_API_KEY already exists.")

    print(f"{INFO}Moving repository contents...")
    move_repository_contents(source_dir, target_dir)

    print(f"{INFO}Adding to system PATH...")
    add_to_path(scripts_dir)

    print(f"{INFO}Creating batch file...")
    create_batch_file(scripts_dir)

    print(f"{SUCCESS}Installation completed successfully.")

if __name__ == "__main__":
    main()
