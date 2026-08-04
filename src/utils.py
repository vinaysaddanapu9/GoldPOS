import tkinter as tk
import json
import os
import sys

def get_base_dir():
    if getattr(sys, "frozen", False):
        # Running as EXE
        return os.path.dirname(sys.executable)
    else:
        # Running from source
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "printer_name": "",
    "less_points": 20,
    "auto_clear": False
}

def ensure_config_exists():
    """
    Creates config.json with default values if it doesn't exist.
    Also adds any missing keys for older config files.
    """

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    updated = False

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            updated = True

    if updated:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    return config

def load_less_points():
    ensure_config_exists()

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    return config["less_points"]

def set_window_size(root, max_width=1000, max_height=650):
    """
    Set responsive window size based on screen resolution.
    """

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = min(max_width, screen_width - 100)
    window_height = min(max_height, screen_height - 100)

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(
        f"{window_width}x{window_height}+{x}+{y}"
    )

    # Minimum size for small screens
    root.minsize(900, 550)

def configure_main_window(root):
    set_window_size(root)

    root.resizable(True, True)
    root.title("GoldPOS v0.1.6")