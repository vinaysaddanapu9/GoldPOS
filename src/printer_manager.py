from tkinter import messagebox
import win32print
import os
import sys
import json

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # EXE folder
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

def get_printer_name():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("printer_name", "")
    return ""

#FOR USB PRINT

printer_name = get_printer_name()
#PRINTER_NAME = "XP-80C (copy 4)"

def print_usb(receipt_text):

    '''printer_name = get_printer_name()

    if not printer_name:
        messagebox.showerror(
            "Printer",
            "No printer configured"
        )
        return'''

    if not receipt_text.strip():

        messagebox.showwarning(
            "Printer",
            "Receipt empty"
        )

        return

    try:

        hprinter = win32print.OpenPrinter(
            printer_name
        )

        try:

            job = win32print.StartDocPrinter(
                hprinter,
                1,
                (
                    "GoldPOS Receipt",
                    None,
                    "RAW"
                )
            )

            win32print.StartPagePrinter(
                hprinter
            )

            data = (
                b"\x1b\x40"
                + receipt_text.strip().encode(
                    "cp437",
                    errors="replace"
                )
                + b"\n\n\n\n\n"
                + b"\x1d\x56\x00"   # ESC/POS full cut
            )

            win32print.WritePrinter(
                hprinter,
                data
            )

            win32print.EndPagePrinter(
                hprinter
            )

            win32print.EndDocPrinter(
                hprinter
            )

        finally:

            win32print.ClosePrinter(
                hprinter
            )

        messagebox.showinfo(
            "Printer",
            "Printed successfully"
        )

    except Exception as e:

        messagebox.showerror(
            "Printer Error",
            str(e)
        )


def test_print(receipt_data):
    print_usb(receipt_data)

# ============================================================
# PRINTER DISCOVERY
# ============================================================

def get_available_printers():
    """
    Return list of installed/connected Windows printers.
    """

    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL
            | win32print.PRINTER_ENUM_CONNECTIONS
        )

        return [printer[2] for printer in printers]

    except Exception:
        return []


def is_printer_available(printer_name=None):
    """
    Check whether the configured printer exists.
    """

    if not printer_name:
        printer_name = get_printer_name()

    if not printer_name:
        return False

    return printer_name in get_available_printers()

def is_auto_clear_enabled():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("auto_clear", False)

    return False
