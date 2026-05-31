import win32print

printers = win32print.EnumPrinters(
    win32print.PRINTER_ENUM_LOCAL
)

for p in printers:
    name = p[2]

    try:
        h = win32print.OpenPrinter(name)

        info = win32print.GetPrinter(h, 2)

        print(
            "OK:",
            name,
            "| Port:",
            info["pPortName"]
        )

        win32print.ClosePrinter(h)

    except Exception as e:

        print(
            "BAD:",
            name,
            "|",
            e
        )