from printer_manager import is_printer_available
import tkinter as tk
import json
import os

CONFIG_FILE = "config.json"


class AboutTab:
    def __init__(self, frame):
        self.frame = frame
        self.printer_status = None
        self.build_ui()

    def load_printer_name(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("printer_name", "")
        return ""

    def save_printer_name(self):
        printer_name = self.printer_var.get().strip()

        data = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)

        data["printer_name"] = printer_name

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.status_label.config(
            text="Printer name saved successfully"
        )

        self.selected_printer_label.config(
            text=f"Selected Printer: {printer_name}"
        )

        # Refresh printer status
        self.update_printer_status()

    def build_ui(self):
        tk.Label(
            self.frame,
            text="About",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        text = """
Jewellery Billing & Gold Exchange Software

✔ Gold Exchange Calculation
✔ Gold Purity Calculation
✔ Receipt Printing
✔ Printer Configuration

Fast • Accurate • Simple
"""

        tk.Label(
            self.frame,
            text=text,
            font=("Segoe UI", 11),
            justify="left",
            wraplength=500
        ).pack(padx=20, pady=10)

        tk.Label(
            self.frame,
            text="Version 0.1.5",
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        # Printer Settings Heading
        tk.Label(
            self.frame,
            text="Printer Settings",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 8))

        # Printer Name
        tk.Label(
            self.frame,
            text="Printer Name",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))

        self.printer_var = tk.StringVar(
            value=self.load_printer_name()
        )

        tk.Entry(
            self.frame,
            textvariable=self.printer_var,
            width=40,
            font=("Arial", 11)
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Save Printer",
            command=self.save_printer_name,
            bg="green",
            fg="white",
            activebackground="dark green",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(pady=8)

        self.status_label = tk.Label(
            self.frame,
            text="",
            fg="green",
            font=("Arial", 10)
        )
        self.status_label.pack()

        # Selected Printer Label
        self.selected_printer_label = tk.Label(
            self.frame,
            text=f"Selected Printer: {self.load_printer_name()}",
            font=("Segoe UI", 10)
        )

        self.selected_printer_label.pack(pady=3)


        # Create Label FIRST
        self.printer_status = tk.Label(
            self.frame,
            text="Printer Status: Checking...",
            font = ("Segoe UI", 10, "bold")
        )

        self.printer_status.pack(pady=5)

        # Then call update
        self.update_printer_status()

        tk.Label(
            self.frame,
            text="© 2026 GoldPOS",
            fg="#555555",
            font=("Segoe UI", 9, "bold")
        ).pack(side="bottom", pady=10)

    def update_printer_status(self):

        printer_name = self.printer_var.get().strip()

        if not printer_name:
            self.printer_status.config(
                text="Printer Status: Not Configured",
                fg="orange"
            )

            return

        if is_printer_available(printer_name):

            self.printer_status.config(
                text="Printer Status: Connected",
                fg="green"
            )

        else:

            self.printer_status.config(
                text="Printer Status: Disconnected",
                fg="red"
            )