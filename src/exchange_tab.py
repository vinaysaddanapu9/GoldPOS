import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .printer_manager import test_print, is_auto_clear_enabled
from .receipt_manager import get_next_receipt_number
from .utils import load_less_points
from .daily_totals import update_daily_totals, get_daily_totals

class ExchangeTab:
    def __init__(self, frame):
        self.frame = frame

        # State
        self.latest_receipt = ""
        self.last_values = None
        self.less_points = load_less_points()

        self.build_ui()

    # ---------------- UI ---------------- #
    def build_ui(self):
        # Main container
        self.home = tk.Frame(self.frame, bg="#f8f5ef")
        self.home.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.home,
            text="Welcome to GoldPOS",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 10))

        # Totals
        total_gold, total_cash, receipt_count = get_daily_totals()

        self.total_gold_label = tk.Label(
            self.home,
            text=f"Gold Exchanged Today : {total_gold:.3f} g",
            font=("Segoe UI", 10, "bold")
        )
        self.total_gold_label.pack()

        self.total_cash_label = tk.Label(
            self.home,
            text=f"Cash Paid Today : ₹ {total_cash:,.2f}",
            font=("Segoe UI", 10, "bold")
        )
        self.total_cash_label.pack(pady=(0, 10))

        self.receipt_count_label = tk.Label(
            self.home,
            text=f"Receipts Today : {receipt_count}",
            font=("Segoe UI", 10, "bold")
        )
        self.receipt_count_label.pack(pady=(0, 10))

        # ---------------- MAIN CONTENT ----------------
        self.content_frame = tk.Frame(self.home, bg="#f8f5ef")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Left panel
        self.left_frame = tk.Frame(
            self.content_frame,
            bg="#f8f5ef",
            bd=1,
            width=380,
            relief=tk.GROOVE
        )

        self.left_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=(0, 10),
            pady=5
        )

        self.left_frame.pack_propagate(False)

        # Right panel
        self.right_frame = tk.Frame(
            self.content_frame,
            bg="#f8f5ef",
            bd=1,
            relief=tk.GROOVE
        )

        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5)

        # ================= INPUT FRAME =================
        # ---------- INPUT SECTION ----------
        tk.Label(
            self.left_frame,
            text="Exchange Details",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f5ef",
            fg="#333333"
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Input frame
        self.input_frame = tk.Frame(self.left_frame, bg="#f8f5ef")
        self.input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Make the column expand
        self.input_frame.grid_columnconfigure(0, weight=1)

        entry_style = {
            "font": ("Segoe UI", 11),
            "relief": tk.SOLID,
            "bd": 1
        }

        # ---------- WEIGHT ----------
        tk.Label(
            self.input_frame,
            text="Impure Gold Weight (g)",
            font=("Segoe UI", 10, "bold"),
            bg="#f8f5ef",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_weight = tk.Entry(self.input_frame, **entry_style)
        self.entry_weight.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 8),
            ipady=6
        )

        # ---------- PURITY ----------
        tk.Label(
            self.input_frame,
            text="Purity %",
            font=("Segoe UI", 10, "bold"),
            bg="#f8f5ef",
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.entry_purity = tk.Entry(self.input_frame, **entry_style)
        self.entry_purity.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 8),
            ipady=6
        )

        # ---------- RATE ----------
        tk.Label(
            self.input_frame,
            text="Rate per Gram (Optional)",
            font=("Segoe UI", 10, "bold"),
            bg="#f8f5ef",
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(0, 5))

        self.entry_rate = tk.Entry(self.input_frame, **entry_style)
        self.entry_rate.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(0, 8),
            ipady=6
        )

        # ================= BUTTON FRAME =================
        # ---------- BUTTONS ----------
        button_container = tk.Frame(self.left_frame, bg="#f8f5ef")
        button_container.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)

        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "relief": tk.FLAT,
            "bd": 0,
            "cursor": "hand2",
            "height": 1
        }

        # Calculate
        tk.Button(
            button_container,
            text="Calculate",
            bg="#0a8f08",
            fg="white",
            activebackground="#087007",
            activeforeground="white",
            command=self.calculate_and_show,
            **button_style
        ).pack(fill=tk.X, pady=2, ipady=4)

        # Print Receipt
        tk.Button(
            button_container,
            text="Print Receipt",
            bg="#d4af37",
            fg="black",
            activebackground="#c19b20",
            command=self.print_receipt,
            **button_style
        ).pack(fill=tk.X, pady=2, ipady=4)

        # ---------- CLEAR + EXIT ROW ----------
        bottom_row = tk.Frame(button_container, bg="#f8f5ef")
        bottom_row.pack(fill=tk.X, pady=(4, 0))

        # Equal width columns
        bottom_row.grid_columnconfigure(0, weight=1)
        bottom_row.grid_columnconfigure(1, weight=1)

        # Clear
        tk.Button(
            bottom_row,
            text="Clear",
            bg="#e5e5e5",
            fg="black",
            activebackground="#d5d5d5",
            command=self.clear_entries,
            **button_style
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4), ipady=4)

        # Exit
        tk.Button(
            bottom_row,
            text="Exit",
            bg="#c62828",
            fg="white",
            activebackground="#a51f1f",
            activeforeground="white",
            command=self.exit_app,
            **button_style
        ).grid(row=0, column=1, sticky="ew", padx=(4, 0), ipady=4)

        # ================= RECEIPT PREVIEW =================
        tk.Label(
            self.right_frame,
            text="Receipt Preview",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f5ef",
            fg="#333333"
        ).pack(anchor="w", padx=15, pady=(15, 10))

        receipt_container = tk.Frame(self.right_frame, bg="#f4f1ea")
        receipt_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(receipt_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.receipt_box = tk.Text(
            receipt_container,
            bg="#fffdf8",
            fg="#222222",
            font=("Consolas", 11),
            wrap=tk.NONE,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=12,
            yscrollcommand=scrollbar.set
        )

        self.receipt_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.receipt_box.yview)

        self.receipt_box.config(state=tk.DISABLED)

    # ---------------- CALCULATE ---------------- #
    def calculate_and_show(self):
        global latest_receipt, last_values

        try:
            impure_weight = float(self.entry_weight.get())
            purity_percent = float(self.entry_purity.get())
            rate_text = self.entry_rate.get().strip()
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
            if current_values == self.last_values:
                return

            # Calculations
            effective_purity = purity_percent

            # Apply less points only for Exchange (no cash rate entered)
            if rate <= 0:
                effective_purity -= (self.less_points / 100)

            pure_weight = impure_weight * (
                    effective_purity / 100
            )

            price = pure_weight * rate if rate > 0 else 0

            # Daily totals
            update_daily_totals(
                pure_weight,
                price
            )

            total_gold, total_cash, receipt_count = get_daily_totals()

            self.total_gold_label.config(
                text=f"Gold Exchanged Today : {total_gold:.3f} g"
            )

            self.total_cash_label.config(
                text=f"Cash Paid Today : ₹ {total_cash:,.2f}"
            )

            self.receipt_count_label.config(
                text=f"Receipts Today : {receipt_count}"
            )

            receipt_no = get_next_receipt_number("EXC")

            today = datetime.now().strftime(
                "%d-%m-%Y %I:%M %p"
            )

            # ---------- RECEIPT PURITY SECTION ----------
            receipt_purity_section = (
                f"{'Purity':<11}: {purity_percent:.2f} %\n"
            )

            if rate <= 0:
                receipt_purity_section += (
                    f"{'Less Points':<11}: {self.less_points / 100:.2f}\n"
                    f"{'Net Purity':<11}: {effective_purity:.2f} %\n"
                )

            # ---------- RATE SECTION ----------
            receipt_rate_section = ""

            if rate > 0:
                receipt_rate_section = (
                    f"\n{'Rate/Gram':<12}: Rs. {rate:,.2f}\n"
                    f"-------------------------------"
                    f"\n{'TOTAL':<12}: Rs. {price:,.2f}"
                )

            # ---------- FINAL RECEIPT ----------
            latest_receipt = (
                "================================\n"
                "             SSJ              \n"
                "        GOLD EXCHANGE         \n"
                "================================\n\n"
                f"{'Receipt No':<12}: {receipt_no}\n"
                f"{'Date':<12}: {today}\n"
                "-------------------------------\n"
                f"{'Impure Wt':<12}: {impure_weight:.3f} g\n"
                f"{receipt_purity_section}"
                f"{'Pure Gold':<12}: {pure_weight:.3f} g"
                f"{receipt_rate_section}\n"
                "================================\n"
                "     Thank You! Visit Again!   \n"
                "       Powered by GoldPOS      \n"
                "================================"
            )

            # Show receipt
            self.receipt_box.config(state=tk.NORMAL)
            self.receipt_box.delete("1.0", tk.END)
            self.receipt_box.insert(
                tk.END,
                latest_receipt
            )
            self.receipt_box.config(state=tk.DISABLED)

            # remember last calculation
            self.last_values = current_values

            self.frame.bell()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers"
            )
    # ---------------- CLEAR ---------------- #
    def clear_entries(self):
        self.last_values = None
        self.latest_receipt = ""

        self.entry_weight.delete(0, tk.END)
        self.entry_purity.delete(0, tk.END)
        self.entry_rate.delete(0, tk.END)

        self.receipt_box.config(state=tk.NORMAL)
        self.receipt_box.delete("1.0", tk.END)
        self.receipt_box.config(state=tk.DISABLED)

        self.entry_weight.focus()

    # ---------------- PRINT ---------------- #
    def print_receipt(self):
        if not self.latest_receipt:
            messagebox.showwarning(
                "Warning",
                "Please calculate first"
            )
            return

        try:
            test_print(self.latest_receipt)

            if is_auto_clear_enabled():
                self.clear_entries()

        except Exception:
            messagebox.showerror(
                "Error",
                "Printer not connected"
            )

    # ---------------- EXIT ---------------- #
    def exit_app(self):
        if messagebox.askyesno(
                "Exit GoldPOS",
                "Are you sure you want to exit?"
        ):
            self.frame.winfo_toplevel().destroy()

