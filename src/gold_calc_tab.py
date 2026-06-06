import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from printer_manager import test_print
from receipt_manager import get_next_receipt_number


today = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

class GoldCalcTab:
    def __init__(self, frame):
        self.frame = frame
        self.rows = []
        self.last_print_text = ""
        self.build_ui()

    # ---------------- UI ---------------- #
    def build_ui(self):
        tk.Label(
            self.frame,
            text="Gold Multi-Row Calculator",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ROW AREA
        self.row_frame = tk.Frame(self.frame)
        self.row_frame.pack(pady=10)

        # BUTTONS
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Row", width=12,
                  command=self.add_row).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Calculate", width=12,
                  command=self.calculate_total).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Preview", width=12,
                  bg="#4a90e2", fg="white",
                  command=self.preview_print).grid(row=0, column=2, padx=5)

        tk.Button(btn_frame, text="Print USB", width=12,
                  bg="#d4af37",
                  command=self.print_to_usb).grid(row=0, column=3, padx=5)

        tk.Button(btn_frame, text="Clear", width=12,
                  bg="#ff4d4d", fg="white",
                  command=self.clear_all).grid(row=0, column=4, padx=5)

        # SUBTRACTION
        sub_frame = tk.Frame(self.frame)
        sub_frame.pack(pady=10)

        tk.Label(sub_frame, text="Subtraction (optional):").grid(row=0, column=0)

        self.sub_entry = tk.Entry(sub_frame, width=10)
        self.sub_entry.grid(row=0, column=1, padx=5)
        self.sub_entry.insert(0, "0")

        # GOLD RATE (optional)
        rate_frame = tk.Frame(self.frame)
        rate_frame.pack(pady=5)

        tk.Label(rate_frame, text="Gold Rate per gram (optional):").grid(row=0, column=0)

        self.rate_entry = tk.Entry(rate_frame, width=10)
        self.rate_entry.grid(row=0, column=1, padx=5)

        # RESULT
        self.result_label = tk.Label(
            self.frame,
            text="Final Total: 0.000 g",
            font=("Arial", 12, "bold")
        )
        self.result_label.pack(pady=10)

        # FIRST ROW
        self.add_row()

    # ---------------- ADD ROW ---------------- #
    def add_row(self):
        row = {}

        frame = tk.Frame(self.row_frame)
        frame.pack(pady=3)

        weight = tk.Entry(frame, width=10)
        weight.grid(row=0, column=0, padx=5)
        weight.insert(0, "0")

        percent = tk.Entry(frame, width=8)
        percent.grid(row=0, column=1, padx=5)
        percent.insert(0, "80")

        row["weight"] = weight
        row["percent"] = percent

        self.rows.append(row)

    # ---------------- SAFE FLOAT ---------------- #
    def safe_float(self, value):
        try:
            return float(value)
        except:
            return 0.0

    # ---------------- CALCULATION ---------------- #
    def calculate_total(self):
        subtotal = 0.0

        sub = self.safe_float(self.sub_entry.get())

        for row in self.rows:
            w = self.safe_float(row["weight"].get())
            p = self.safe_float(row["percent"].get())
            subtotal += w * (p / 100)

        total = subtotal - sub
        if total < 0:
            total = 0

        rate = self.safe_float(self.rate_entry.get())
        value = total * rate if rate > 0 else None

        self.result_label.config(text=f"Final Total: {total:.3f} g")

        self.last_print_text = self.build_print_text(subtotal, sub, total, rate, value)

    # ---------------- RECEIPT ---------------- #
    def build_print_text(self, subtotal, sub, total, rate, value):
        text = "\n"
        text += "=======================================\n"
        text += "   SSJ ROUGH ESTIMATE \n"
        text += "=======================================\n\n"
        text += "Receipt No : " + get_next_receipt_number("GLD") + "\n"
        text += "Date : " + today + "\n\n"

        for i, row in enumerate(self.rows, start=1):
            try:
                w = self.safe_float(row["weight"].get())
                p = self.safe_float(row["percent"].get())
                pure = w * (p / 100)

                text += f"{'Item '+str(i):<6}{w:>8.3f} x {p:>5}% = {pure:>8.3f}g\n"
            except:
                pass

        text += "\n-------------------------------------\n"
        text += f"{'Subtotal':<18}: {subtotal:>10.3f} g\n"

        if sub > 0:
            text += f"{'Subtraction':<18}: -{sub:>9.3f} g\n"

        text += "-------------------------------------\n"
        text += f"{'FINAL TOTAL':<18}: {total:>10.3f} g\n"

        # OPTIONAL GOLD VALUE
        if rate > 0:
            text += f"{'Gold Rate':<18}: {rate:>10.2f} /g\n"
            text += f"{'Total Value':<18}: {value:>10.2f}\n"

        text += "====================================\n"
        text += "     Thank You! Visit Again! \n"
        text += "     Powered by GoldPOS \n"
        text += "====================================\n"

        return text

    # ---------------- PRINT ---------------- #
    def print_to_usb(self):
        if not self.last_print_text:
            messagebox.showwarning("Warning", "Please calculate first")
            return

        try:
            test_print(self.last_print_text)
        except:
            messagebox.showerror("Error", "Printer not connected")

    # ---------------- PREVIEW ---------------- #
    def preview_print(self):
        if not self.last_print_text:
            messagebox.showwarning("Warning", "Please calculate first")
            return

        preview = tk.Toplevel(self.frame)
        preview.title("Print Preview")
        preview.geometry("450x550")

        font_style = ("Courier New", 10)

        scrollbar = tk.Scrollbar(preview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_box = tk.Text(
            preview,
            wrap=tk.NONE,
            yscrollcommand=scrollbar.set,
            font=font_style
        )
        text_box.pack(expand=True, fill="both")

        scrollbar.config(command=text_box.yview)

        text_box.insert(tk.END, self.last_print_text)
        text_box.config(state=tk.DISABLED)

    # ---------------- CLEAR ---------------- #
    def clear_all(self):
        for widget in self.row_frame.winfo_children():
            widget.destroy()

        self.rows.clear()

        self.sub_entry.delete(0, tk.END)
        self.sub_entry.insert(0, "0")

        self.rate_entry.delete(0, tk.END)

        self.result_label.config(text="Final Total: 0.000 g")

        self.last_print_text = ""

        self.add_row()