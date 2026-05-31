from tkinter import messagebox
import win32print

#FOR USB PRINT

PRINTER_NAME = "XP-80C (copy 4)"

def print_usb(receipt_text):

    if not receipt_text.strip():

        messagebox.showwarning(
            "Printer",
            "Receipt empty"
        )

        return

    try:

        hprinter = win32print.OpenPrinter(
            PRINTER_NAME
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

    sample = """
========================
       GOLDPOS
========================

Thermal Test

Weight : 12.500 g
Rate   : 9850

Total  : 123125

========================
"""

    print_usb(receipt_data)

def print_bt(receipt_text):
    print_usb(receipt_text)