import tkinter as tk
import json

CONFIG_FILE = "config.json"

def load_less_points():
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