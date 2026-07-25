import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tabs import AppTabs
from settings import SettingsTab
from about import AboutTab
from printer_manager import test_print
from gold_calc_tab import GoldCalcTab
from receipt_manager import get_next_receipt_number
from utils import load_less_points, configure_main_window
import ctypes
import os


from daily_totals import (
    update_daily_totals,
    get_daily_totals
)

# Global receipt text
latest_receipt = ""
RECEIPT_FILE = "../data/receipt_counter.txt"

# Prevent duplicate calculate clicks
last_values = None

def get_receipt_text():
    return receipt_box.get("1.0", "end-1c")

less_points = load_less_points()

# ---------------- CALCULATE ---------------- #
def calculate_and_show():
    global latest_receipt, last_values

    try:
        impure_weight = float(entry_weight.get())
        purity_percent = float(entry_purity.get())
        rate_text = entry_rate.get().strip()
        rate = float(rate_text) if rate_text else 0

        if impure_weight <= 0 or purity_percent <= 0:
            messagebox.showerror(
                "Error",
                "Values must be greater than 0"
            )
            return

        current_values = (
            impure_weight,
            purity_percent,
            rate
        )

        # Ignore duplicate clicks
        if current_values == last_values:
            return

        # Calculations
        effective_purity = purity_percent

        # Apply less points only for Exchange (no cash rate entered)
        if rate <= 0:
            effective_purity -= (less_points / 100)

        pure_weight = impure_weight * (
                effective_purity / 100
        )

        price = pure_weight * rate if rate > 0 else 0

        # Daily totals
        update_daily_totals(
            pure_weight,
            price
        )

        total_gold, total_cash = get_daily_totals()

        total_gold_label.config(
            text=f"Gold Exchanged Today : {total_gold:.3f} g"
        )

        total_cash_label.config(
            text=f"Cash Paid Today : ₹ {total_cash:,.2f}"
        )

        receipt_no = get_next_receipt_number("EXC")

        today = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        # Receipt purity section
        receipt_purity_section = (
            f"{'Purity':<11}: {purity_percent:.2f} %\n"
        )

        if rate <= 0:
            receipt_purity_section += (
                f"{'Less Points':<11}: {less_points / 100:.2f}\n"
                f"{'Net Purity':<11}: {effective_purity:.2f} %\n"
            )

        receipt_rate_section = ""

        if rate > 0:
            receipt_rate_section = f"""
Rate/Gram  : Rs. {rate:,.2f}

TOTAL      : Rs. {price:,.2f}
"""

        latest_receipt = f"""
================================
           SSJ
      ROUGH ESTIMATE
================================

Receipt No : {receipt_no}
Date       : {today}

Impure Wt  : {impure_weight:.3f} g
{receipt_purity_section}Pure Gold  : {pure_weight:.3f} g
{receipt_rate_section}
================================
   Thank You! Visit Again!
   Powered by GoldPOS
================================
"""

        # Show receipt
        receipt_box.config(state= tk.NORMAL)
        receipt_box.delete("1.0", tk.END)
        receipt_box.insert(
            tk.END,
            latest_receipt
        )
        receipt_box.config(state= tk.DISABLED)

        # remember last calculation
        last_values = current_values

        root.bell()

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers"
        )


# ---------------- CLEAR ---------------- #
def clear_exchange_entries():
    global latest_receipt, last_values

    last_values = None

    entry_weight.delete(0, tk.END)
    entry_purity.delete(0, tk.END)
    entry_rate.delete(0, tk.END)

    receipt_box.config(state= tk.NORMAL)
    receipt_box.delete("1.0", tk.END)
    receipt_box.config(state= tk.DISABLED)

    latest_receipt = ""

    entry_weight.focus()

# ---------------- EXIT ---------------- #
def exit_app():
    if messagebox.askyesno(
            "Exit GoldPOS",
            "Are you sure you want to exit?"
    ):
        root.destroy()

# ---------------- MAIN WINDOW ---------------- #
myapp_id = "GoldPOS.app.v1"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)

root = tk.Tk()
icon_path = os.path.abspath("GoldPOS.ico")

style = ttk.Style()
style.theme_use("clam")

root.title("GoldPOS v0.1.6")
root.iconbitmap(icon_path)

root.configure(bg="#f8f5ef")
configure_main_window(root)

# Load tabs
app = AppTabs(root)
home = app.home_tab
gold_calc = GoldCalcTab(app.gold_calc_tab)
settings = SettingsTab(app.settings_tab)
about = AboutTab(app.about)

tk.Label(
    home,
    text="Welcome to GoldPOS",
    font=("Segoe UI", 14, "bold"),
    bg="#f8f5ef",
    fg="#333333"
).pack(pady=(15, 10))

#FOOTER
footer = tk.Label(
    root,
    text="GoldPOS v0.1.6 | Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor="w",
    padx=10,
    font=("Segoe UI", 8),  # normal font
    fg="black"
)

footer.pack(
    side=tk.BOTTOM,
    fill=tk.X
)

# ---------------- TOTALS ---------------- #
total_gold, total_cash = get_daily_totals()

total_gold_label = tk.Label(
    home,
    text=f"Gold Exchanged Today : {total_gold:.3f} g",
    font=("Segoe UI", 10, "bold"),
    bg="#f4f1ea",
    fg="#333333"
)

total_gold_label.pack()

total_cash_label = tk.Label(
    home,
    text=f"Cash Paid Today : ₹ {total_cash:,.2f}",
    font=("Segoe UI", 10, "bold"),
    bg="#f4f1ea",
    fg="green"
)

total_cash_label.pack(
    pady=(0, 10)
)

# ---------------- INPUT FRAME ---------------- #
input_frame = tk.Frame(
    home,
    bg="#f8f5ef"
)

input_frame.pack(pady=10)

# Weight
tk.Label(
    input_frame,
    text="Impure Gold Weight (g)",
    font=("Segoe UI", 11),
    bg="#f8f5ef"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky=tk.W
)

entry_weight = tk.Entry(
    input_frame,
    width=20,
    font=("Segoe UI", 11)
)

entry_weight.grid(
    row=0,
    column=1,
    padx=10
)

# Purity
tk.Label(
    input_frame,
    text="Purity %",
    font=("Segoe UI", 11),
    bg="#f8f5ef"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky=tk.W
)

entry_purity = tk.Entry(
    input_frame,
    width=20,
    font=("Segoe UI", 11)
)

entry_purity.grid(
    row=1,
    column=1,
    padx=10
)

# Rate
tk.Label(
    input_frame,
    text="Rate per Gram (Optional)",
    font=("Segoe UI", 11),
    bg="#f8f5ef"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky=tk.W
)

entry_rate = tk.Entry(
    input_frame,
    width=20,
    font=("Segoe UI", 11)
)

entry_rate.grid(
    row=2,
    column=1,
    padx=10
)

# Focus movement
entry_weight.bind(
    "<Return>",
    lambda e: entry_purity.focus()
)

entry_purity.bind(
    "<Return>",
    lambda e: entry_rate.focus()
)

entry_rate.bind(
    "<Return>",
    lambda e: calculate_and_show()
)

entry_weight.focus()

# ---------------- BUTTONS ---------------- #
button_frame = tk.Frame(
    home,
    bg="#f8f5ef"
)

button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Calculate",
    width=15,
    bg="green",
    fg="white",
    font=("Arial", 10, "bold"),
    command=calculate_and_show
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

#Clear
tk.Button(
    button_frame,
    text="Clear",
    width=15,
    font=("Arial", 10, "bold"),
    command=clear_exchange_entries
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

# Print
tk.Button(
    button_frame,
    text="Print Receipt",
    width=15,
    bg="#d4af37",
    fg="black",
    font=("Arial", 10, "bold"),
    command=lambda: test_print(latest_receipt)
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

#Exit
tk.Button(
    button_frame,
    text="Exit",
    width=15,
    bg="#C62828",
    fg="white",
    font=("Arial", 10, "bold"),
    command=exit_app
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

# ---------------- RECEIPT BOX ---------------- #
tk.Label(
    home,
    text="Receipt Preview",
    font=("Segoe UI", 12, "bold"),
    bg="#f8f5ef"
).pack()

receipt_frame = tk.Frame(
    home,
    bg="#f4f1ea"
)

receipt_frame.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

scrollbar = tk.Scrollbar(
    receipt_frame
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

receipt_box = tk.Text(
    receipt_frame,
    width=60,
    height=12,
    bg="#fffdf8",
    font=("Courier New", 10),
    yscrollcommand=scrollbar.set,
    relief=tk.SOLID,
    bd=1
)

receipt_box.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

scrollbar.config(
    command=receipt_box.yview
)

receipt_box.config(
    state=tk.DISABLED
)

# ---------------- RUN ---------------- #
root.mainloop()