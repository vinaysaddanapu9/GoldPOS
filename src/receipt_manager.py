import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECEIPT_FILE = os.path.join(BASE_DIR, "receipt_counter.txt")

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