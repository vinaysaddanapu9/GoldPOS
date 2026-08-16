import tkinter as tk
from tkinter import ttk

class AppTabs:
    def __init__(self, root):

        style = ttk.Style()
        style.theme_use("clam")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )

        # Tabs
        self.exchange_tab = tk.Frame(self.notebook, bg="#f8f5ef")
        self.gold_calc_tab = tk.Frame(self.notebook, bg="#f8f5ef")
        self.settings_tab = tk.Frame(self.notebook, bg="#f8f5ef")
        self.about = tk.Frame(self.notebook, bg="#f8f5ef")

        self.notebook.add(self.exchange_tab, text="Exchange")
        self.notebook.add(self.gold_calc_tab, text="Gold Calc")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.about, text="About")