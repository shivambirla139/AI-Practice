import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# ANSI escape sequences for coloring
START_SEQUENCE = "\033[90m"  # Gray / Dim color for debug logs
END_SEQUENCE = "\033[0m"


def log(msg: str):
    """
    Prints debug messages if Debug is set to True in the .env file.
    """
    debug_mode = os.getenv("Debug", "False").strip().lower() in ["true", "1", "yes"]
    if debug_mode:
        print(f"{START_SEQUENCE}{msg}{END_SEQUENCE}")
