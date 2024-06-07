import os
import shutil
import subprocess
import sys

# Simple color print functions without dependencies
def print_info(message):
    print("\033[96m{}\033[0m".format(message))

def print_warning(message):
    print("\033[93m{}\033[0m".format(message))

def print_error(message):
    print("\033[91m{}\033[0m".format(message))

def print_success(message):
    print("\033[92m{}\033[0m".format(message))

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print_error("Failed to install dependencies. Error: {}".format(e))
        sys.exit(1)

def set_environment_variable(key, value):
    os.environ[key] = value
    shell_config = os.path.expanduser("~/.zshrc" if os.environ.get("SHELL", "").endswith("zsh") else "~/.bash_profile")
    with open(shell_config, "a") as file:
        file.write(f"\nexport {key}={value}\n")
    print_success("Environment variable {} set to: {}".format(key, value))

def on_rm_error(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def move_repository_contents(source_dir, target_dir):
    if os.path.exists(target_dir):
        print_warning("Removing existing directory at {}".format(target_dir))
        shutil.rmtree(target_dir, onerror=on_rm_error)
    os.makedirs(target_dir)
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print_success("Repository contents moved to {}".format(target_dir))

def add_to_path(directory):
    shell_config = os.path.expanduser("~/.zshrc" if os.environ.get("SHELL", "").endswith("zsh") else "~/.bash_profile")
    with open(shell_config, "a") as file:
        file.write(f'\nexport PATH="$PATH:{directory}"\n')
    print_success("Added {} to system PATH.".format(directory))

def create_script_file(directory):
    script_content = "#!/bin/bash\npython3 {}/ai_diff_commit/src/ai_diff_commit.py $*\n".format(directory)
    script_file_path = os.path.join(directory, "ai_diff_commit.sh")
    with open(script_file_path, "w") as script_file:
        script_file.write(script_content)
    os.chmod(script_file_path, 0o755)
    print_success("Script file created at {}".format(script_file_path))

def create_alias(scripts_dir):
    shell_config = os.path.expanduser("~/.zshrc" if os.environ.get("SHELL", "").endswith("zsh") else "~/.bash_profile")
    alias_command = f"alias ai_diff_commit='{scripts_dir}/ai_diff_commit.sh'\n"
    with open(shell_config, "a") as file:
        file.write(alias_command)
    print_success("Alias for ai_diff_commit added to {}".format(shell_config))

def source_shell_config():
    shell = os.environ.get("SHELL", "")
    shell_config = os.path.expanduser("~/.zshrc" if shell.endswith("zsh") else "~/.bash_profile")
    if shell.endswith("zsh"):
        try:
            subprocess.check_call(["zsh", "-c", f"source {shell_config}"])
            print_success(f"Sourced {shell_config} to apply changes.")
        except subprocess.CalledProcessError:
            print_warning(f"Failed to source {shell_config}. Please run 'source {shell_config}' manually.")
    else:
        print_warning(f"Automatic sourcing is not supported for the current shell ({shell}). Please run 'source {shell_config}' manually.")

def main():
    clear_console()
    source_dir = os.getcwd()
    home_dir = os.path.expanduser("~")
    scripts_dir = os.path.join(home_dir, "Scripts")
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
    create_script_file(scripts_dir)

    print_info("Creating alias for the command...")
    create_alias(scripts_dir)

    print_info("Sourcing shell configuration file to apply changes...")
    source_shell_config()

    print_success("Installation completed successfully. If the command 'ai_diff_commit' is still not found, please restart your terminal or run 'source ~/.zshrc' or 'source ~/.bash_profile' manually.")

if __name__ == "__main__":
    main()
