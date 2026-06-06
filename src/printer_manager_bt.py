import win32print
import win32ui

def print_receipt(text):
    printer_name = win32print.GetDefaultPrinter()

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    hdc.StartDoc("GoldPOS Receipt")
    hdc.StartPage()

    x = 50
    y = 50
    line_height = 30

    for line in text.split("\n"):
        hdc.TextOut(x, y, line)
        y += line_height

    hdc.EndPage()
    hdc.EndDoc()
