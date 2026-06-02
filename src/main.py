import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tabs import AppTabs
from about import AboutTab
from printer_manager import print_bt, test_print
from gold_rate_widget import create_gold_rate_ui
from gold_calc_tab import GoldCalcTab
from receipt_manager import get_next_receipt_number
import ctypes
import os

from daily_totals import (
    update_daily_totals,
    get_daily_totals
)

# Global receipt text
latest_receipt = ""
RECEIPT_FILE = "receipt_counter.txt"

# Prevent duplicate calculate clicks
last_values = None

def get_receipt_text():
    return receipt_box.get("1.0", "end-1c")


# ---------------- CALCULATE ---------------- #
def calculate_and_show():
    global latest_receipt, last_values

    try:
        impure_weight = float(entry_weight.get())
        purity_percent = float(entry_purity.get())
        rate = float(entry_rate.get())

        if impure_weight <= 0 or purity_percent <= 0 or rate <= 0:
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
        pure_weight = impure_weight * (
            purity_percent / 100
        )

        price = pure_weight * rate

        # Daily totals
        update_daily_totals(
            pure_weight,
            price
        )

        total_gold, total_cash = get_daily_totals()

        total_gold_label.config(
            text=f"Today's Gold Exchange : {total_gold:.3f} g"
        )

        total_cash_label.config(
            text=f"Today's Cash : ₹ {total_cash:.2f}"
        )

        receipt_no = get_next_receipt_number("EXC")

        today = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        latest_receipt = f"""
================================
           SSJ
      ROUGH ESTIMATE
================================

Receipt No : {receipt_no}
Date       : {today}

Impure Wt  : {impure_weight:.3f} g
Purity     : {purity_percent:.2f} %

Pure Gold  : {pure_weight:.3f} g

Rate/Gram  : Rs. {rate:.2f}

TOTAL      : Rs. {price:.2f}

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
def clear_entries():
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
    root.destroy()

# ---------------- MAIN WINDOW ---------------- #
myapp_id = "GoldPOS.app.v1"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)

root = tk.Tk()
icon_path = os.path.abspath("GoldPOS.ico")

style = ttk.Style()
style.theme_use("clam")

root.title("GoldPOS v0.0.1")
root.iconbitmap(icon_path)
root.geometry("520x650")

root.configure(bg="#f8f5ef")
root.resizable(False, False)

# Load tabs
app = AppTabs(root)
home = app.home_tab
gold_calc = GoldCalcTab(app.gold_calc_tab)
about = AboutTab(app.about)

# ---------------- LIVE GOLD RATE ---------------- #
create_gold_rate_ui(home)

# ---------------- TOTALS ---------------- #
total_gold, total_cash = get_daily_totals()

total_gold_label = tk.Label(
    home,
    text=f"Today's Gold Exchange : {total_gold:.3f} g",
    font=("Segoe UI", 11, "bold"),
    bg="#f4f1ea",
    fg="#333333"
)

total_gold_label.pack()

total_cash_label = tk.Label(
    home,
    text=f"Today's Cash : ₹ {total_cash:.2f}",
    font=("Segoe UI", 11, "bold"),
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
    text="Rate per Gram",
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
    command=clear_entries
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

# Print USB
tk.Button(
    button_frame,
    text="Print USB",
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

# Print Bluetooth
tk.Button(
    button_frame,
    text="Print BT",
    width=15,
    bg="#005A9C",
    fg="black",
    font=("Arial", 10, "bold"),
    command=lambda: print_bt(latest_receipt)
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

#Exit
tk.Button(
    button_frame,
    text="Exit",
    width=32,
    bg="#C62828",
    fg="white",
    font=("Arial", 10, "bold"),
    command=exit_app
).grid(
    row=2,
    column=0,
    columnspan=2,
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
    height=20,
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