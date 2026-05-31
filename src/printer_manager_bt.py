from tkinter import *
from datetime import datetime

# FOR BLUETOOTH PRINT

def calculate_and_show():
    try:
        # Read inputs
        impure_weight = float(entry_weight.get())
        purity_percent = float(entry_purity.get())
        rate = float(entry_rate.get())

        # Calculate pure gold and price
        pure_weight = impure_weight * (purity_percent / 100)
        price = pure_weight * rate

        # Get today's date
        today = datetime.now().strftime("%d-%m-%Y")

        # Format receipt
        receipt_text = f"""
        SADDANAPU SHANKER JWELLERY WORKS
        Date: {today}

        Impure Gold Weight: {impure_weight} g
        Purity: {purity_percent} %
        Pure Gold Weight: {pure_weight:.2f} g
        Rate per Gram: {rate}
        Total Price: {price:.2f}

        Thank you!
        """

        # Show receipt in popup
        popup = Toplevel()
        popup.title("Receipt")
        receipt_label = Label(popup, text=receipt_text, justify=LEFT, font=("Courier", 12))
        receipt_label.pack(padx=10, pady=10)

        # Close button in receipt popup
        Button(popup, text="Close", command=popup.destroy).pack(pady=5)

        # Copy receipt to clipboard for RawBT printing
        popup.clipboard_clear()
        popup.clipboard_append(receipt_text)
        popup.update()  # Ensure clipboard is updated

    except ValueError:
        error_popup = Toplevel()
        error_popup.title("Error")
        Label(error_popup, text="Please enter valid numbers").pack(padx=10, pady=10)
        Button(error_popup, text="Close", command=error_popup.destroy).pack(pady=5)


def clear_entries():
    """Clear all input fields"""
    entry_weight.delete(0, END)
    entry_purity.delete(0, END)
    entry_rate.delete(0, END)


def exit_app():
    """Exit the application"""
    root.destroy()


# Main GUI
root = Tk()
root.title("Gold Calculator")

labels = ["Impure Gold Weight (g)", "Purity %", "Rate per Gram"]
entries = []

for i, label in enumerate(labels):
    Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=W)
    entry = Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

entry_weight, entry_purity, entry_rate = entries

# Buttons with spacing
button_frame = Frame(root)
button_frame.grid(row=len(labels), columnspan=2, pady=15)

Button(button_frame, text="Calculate & Show Receipt", width=20, command=calculate_and_show).grid(row=0, column=0,
                                                                                                 padx=5)
Button(button_frame, text="Clear", width=10, command=clear_entries).grid(row=0, column=1, padx=5)
Button(button_frame, text="Exit", width=10, command=exit_app).grid(row=0, column=2, padx=5)

root.mainloop()
