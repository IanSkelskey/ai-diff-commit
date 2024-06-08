"""
Color Constants

This module defines color constants for use in terminal output.

Attributes:
    INFO: Information color.
    GIT_INFO: Git information color.
    AI_INFO: AI information color.
    GENERATED: Generated message color.
    WARNING: Warning message color.
    ERROR: Error message color.
    SUCCESS: Success message color.
    RESET: Reset color.
"""

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
