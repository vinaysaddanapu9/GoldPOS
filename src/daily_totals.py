import os
import sys
import json
from datetime import datetime

# Folder
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.dirname(BASE_DIR)

DAILY_FOLDER = os.path.join(
    PROJECT_DIR,
    "data",
    "daily_sales"
)

# Create folder if it doesn't exist
os.makedirs(DAILY_FOLDER, exist_ok=True)


def get_today_file():
    today = datetime.now().strftime("%Y-%m-%d")

    return os.path.join(
        DAILY_FOLDER,
        f"{today}.json"
    )


def initialize_daily_file():
    filepath = get_today_file()

    if not os.path.exists(filepath):
        data = {
            "total_gold": 0.0,
            "total_cash": 0.0,
            "receipt_count": 0
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)


def get_daily_totals():
    initialize_daily_file()

    filepath = get_today_file()

    with open(filepath, "r") as f:
        data = json.load(f)

    total_gold = float(data.get("total_gold", 0.0))
    total_cash = float(data.get("total_cash", 0.0))
    receipt_count = int(data.get("receipt_count", 0))

    return total_gold, total_cash, receipt_count


def update_daily_totals(pure_gold, cash):
    initialize_daily_file()

    filepath = get_today_file()

    total_gold, total_cash, receipt_count = get_daily_totals()

    total_gold += pure_gold
    total_cash += cash
    receipt_count += 1

    data = {
        "total_gold": total_gold,
        "total_cash": total_cash,
        "receipt_count": receipt_count
    }

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)