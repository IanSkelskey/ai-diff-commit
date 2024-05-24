from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define color constants
INFO = Fore.CYAN
GIT_INFO = Fore.BLUE
AI_INFO = Style.BRIGHT + Fore.MAGENTA
GENERATED = Fore.MAGENTA
WARNING = Fore.YELLOW
ERROR = Fore.RED
SUCCESS = Fore.GREEN
RESET = Style.RESET_ALL
