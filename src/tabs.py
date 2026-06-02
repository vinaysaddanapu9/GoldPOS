import tkinter as tk
from tkinter import ttk

class AppTabs:
    def __init__(self, root):

        style = ttk.Style()
        style.theme_use("clam")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.home_tab = tk.Frame(self.notebook, bg="#f8f5ef")
        self.gold_calc_tab = tk.Frame(self.notebook, bg="#f8f5ef")
        self.about = tk.Frame(self.notebook, bg="#f8f5ef")

        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.gold_calc_tab, text="Gold Calc")
        self.notebook.add(self.about, text="About")