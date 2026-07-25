import tkinter as tk


class AboutTab:

    def __init__(self, frame):
        self.frame = frame
        self.build_ui()


    def build_ui(self):

        # App Name
        tk.Label(
            self.frame,
            text="GoldPOS",
            font=("Arial", 24, "bold"),
            fg="#B8860B"
        ).pack(pady=(30, 5))


        tk.Label(
            self.frame,
            text="Jewellery Management Software",
            font=("Segoe UI", 12, "bold")
        ).pack()


        # Short Description
        tk.Label(
            self.frame,
            text=(
                "A simple solution for gold calculation,\n"
                "purity checking and receipt printing."
            ),
            font=("Segoe UI", 11),
            justify="center"
        ).pack(pady=25)


        # Version
        tk.Label(
            self.frame,
            text="Version 0.1.6",
            font=("Segoe UI", 12, "bold"),
            fg="green"
        ).pack(pady=10)


        # Footer
        tk.Label(
            self.frame,
            text="Powered by GoldPOS",
            font=("Segoe UI", 10, "bold"),
            fg="#555555"
        ).pack(
            side="bottom",
            pady=20
        )


        tk.Label(
            self.frame,
            text="© 2026",
            font=("Segoe UI", 9),
            fg="#777777"
        ).pack(
            side="bottom"
        )