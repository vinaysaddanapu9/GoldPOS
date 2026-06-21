import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.dirname(BASE_DIR)

RECEIPT_FILE = os.path.join(
    PROJECT_DIR,
    "data",
    "receipt_counter.txt"
)

# ---------------- RECEIPT NUMBER ---------------- #
def get_next_receipt_number(receipt_type):
    # Create file if missing
    if not os.path.exists(RECEIPT_FILE):
        with open(RECEIPT_FILE, "w") as f:
            f.write("1")

    # Read current counter
    with open(RECEIPT_FILE, "r") as f:
        counter = int(f.read().strip())

    # Generate receipt number
    receipt_no = f"{receipt_type}-{counter:04d}"

    # Save next counter
    with open(RECEIPT_FILE, "w") as f:
        f.write(str(counter + 1))

    return receipt_no