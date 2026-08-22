import tkinter as tk
from tkinter import ttk
import ctypes
import os
from src.exchange_tab import ExchangeTab
from src.gold_calc_tab import GoldCalcTab
from src.settings import SettingsTab
from src.about import AboutTab
from src.tabs import AppTabs
from src.utils import configure_main_window, ensure_config_exists,resource_path

# Ensure config exists
ensure_config_exists()

# ---------------- MAIN WINDOW ---------------- #
myapp_id = "GoldPOS.app.v1"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)

root = tk.Tk()

icon_path = resource_path(os.path.join("assets", "goldpos.ico"))

if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

style = ttk.Style()
style.theme_use("clam")

root.title("GoldPOS v0.1.7")

root.configure(bg="#f8f5ef")
configure_main_window(root)

# Tabs
app = AppTabs(root)

# Load tab classes
exchange = ExchangeTab(app.exchange_tab)
gold_calc = GoldCalcTab(app.gold_calc_tab)
settings = SettingsTab(app.settings_tab)
about = AboutTab(app.about)

# Footer
footer = tk.Label(
    root,
    text="GoldPOS v0.1.6 | Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor="w",
    padx=10,
    font=("Segoe UI", 8),
    fg="black"
)

footer.pack(side=tk.BOTTOM, fill=tk.X)

# ---------------- RUN ---------------- #
root.mainloop()