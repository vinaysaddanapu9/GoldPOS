import tkinter as tk

class AboutTab:
    def __init__(self, frame):
        self.frame = frame
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.frame,
            text="About GoldPOS",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        text = """
GoldPOS is a Jewellery Billing System designed for small and medium shops.

✔ Performs gold exchange calculations
✔ Calculates pure gold weight based on purity
✔ Generates automatic receipts with unique numbers
✔ Maintains daily gold and cash totals
✔ Supports USB thermal printer printing
✔ Supports Bluetooth printer printing

This system helps simplify jewellery billing operations
and reduces manual calculation errors.
        """

        tk.Label(
            self.frame,
            text=text,
            font=("Arial", 11),
            justify="left",
            wraplength=500
        ).pack(padx=20, pady=10)

        tk.Label(
            self.frame,
            text="Version 0.0.1",
            font=("Arial", 10, "bold")
        ).pack(pady=5)