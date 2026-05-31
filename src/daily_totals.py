import os
from datetime import datetime

# Folder
DAILY_FOLDER = "daily_sales"

# Create folder if missing
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