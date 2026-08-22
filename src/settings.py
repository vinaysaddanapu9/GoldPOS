from .printer_manager import is_printer_available
import tkinter as tk
import json
import os

CONFIG_FILE = "config.json"

class SettingsTab:
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

    def load_organization_name(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("organization_name", "SSJ")
        return "SSJ"

    def load_less_points(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("less_points", "0.30")
        return "0.30"

    def load_auto_clear(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("auto_clear", False)
        return False

    def save_organization(self):
        organization_name = self.organization_var.get().strip()

        data = {}

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)

        data["organization_name"] = organization_name

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.status_label.config(
            text="Organization name saved successfully",
            fg="green"
        )

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

    def save_exchange_settings(self):
        data = {}

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)

        data["less_points"] = int(self.less_points_var.get())
        data["auto_clear"] = self.auto_clear_var.get()

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.status_label.config(
            text="Exchange settings saved successfully",
            fg="green"
        )

    def build_ui(self):
        # ==========================
        # Organization Settings
        # ==========================

        tk.Label(
            self.frame,
            text="Organization Name",
            font=("Arial", 11, "bold")
        ).pack(pady=(10, 5))

        self.organization_var = tk.StringVar(
            value=self.load_organization_name()
        )

        tk.Entry(
            self.frame,
            textvariable=self.organization_var,
            width=40,
            font=("Arial", 11)
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Save Organization",
            command=self.save_organization,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18
        ).pack(pady=(5, 15))


        # ==========================
        # Exchange Settings
        # ==========================

        tk.Label(
            self.frame,
            text="Exchange Settings",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 8))

        tk.Label(
            self.frame,
            text="Less Points (%)",
            font=("Arial", 11, "bold")
        ).pack()

        self.less_points_var = tk.StringVar(
            value=self.load_less_points()
        )

        tk.Entry(
            self.frame,
            textvariable=self.less_points_var,
            width=20,
            font=("Arial", 11)
        ).pack(pady=5)

        self.auto_clear_var = tk.BooleanVar(
            value=self.load_auto_clear()
        )

        tk.Checkbutton(
            self.frame,
            text="Auto Clear After Print",
            variable=self.auto_clear_var,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=20, pady=10)

        tk.Button(
            self.frame,
            text="Save Exchange",
            command=self.save_exchange_settings,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(pady=(5, 15))

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