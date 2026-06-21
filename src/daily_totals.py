import os
import sys
from datetime import datetime

# Folder
if getattr(sys, 'frozen', False):
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
if not os.path.exists(DAILY_FOLDER):
    os.makedirs(DAILY_FOLDER)

def get_today_file():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(
        DAILY_FOLDER,
        f"{today}.txt"
    )


def initialize_daily_file():
    filepath = get_today_file()

    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write("0,0")


def get_daily_totals():
    initialize_daily_file()

    filepath = get_today_file()

    with open(filepath, "r") as f:
        data = f.read().split(",")

    total_gold = float(data[0])
    total_cash = float(data[1])

    return total_gold, total_cash


def update_daily_totals(pure_gold, cash):
    initialize_daily_file()

    filepath = get_today_file()

    total_gold, total_cash = get_daily_totals()

    total_gold += pure_gold
    total_cash += cash

    with open(filepath, "w") as f:
        f.write(f"{total_gold},{total_cash}")