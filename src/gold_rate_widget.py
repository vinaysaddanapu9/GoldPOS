# gold_rate_widget.py

from tkinter import Label
import urllib.request
import json
import threading
import time

last_rate = None
latest_rate = None


def fetch_gold_rate():
    """
    Fetch live gold price and return INR per gram.
    """

    global last_rate

    try:
        url = "https://api.gold-api.com/price/XAU/INR"

        response = urllib.request.urlopen(url, timeout=5)
        data = json.loads(response.read())

        usd_ounce = float(data["price"])

        usd_to_inr = 84.0  # you can also make this dynamic later

        gram_rate = (usd_ounce / 31.1035) * usd_to_inr
        gram_rate = round(gram_rate, 2)

        if last_rate is None:
            change = 0
        else:
            change = gram_rate - last_rate

        last_rate = gram_rate

        return gram_rate, change

    except:
        return None, 0


def _background_fetch(label, root):
    """
    Runs in background thread and updates UI safely
    """

    global latest_rate

    while True:
        rate, change = fetch_gold_rate()

        if rate is not None:
            latest_rate = (rate, change)

            root.after(0, update_ui, label, rate, change)

        time.sleep(15)  # refresh interval


def update_ui(label, rate, change):

    if rate is None:
        label.config(text="Gold Rate: offline", fg="gray")
        return

    if change > 0:
        color = "#d32f2f"
        arrow = "▲"
    elif change < 0:
        color = "#2e7d32"
        arrow = "▼"
    else:
        color = "black"
        arrow = "•"

    label.config(
        text=f"24K Gold: ₹ {rate:.2f}/g {arrow}",
        fg=color
    )


def create_gold_rate_ui(root):

    label = Label(
        root,
        text="Loading gold rate...",
        font=("Arial", 11, "bold"),
        bg="#f8f5ef"
    )

    label.pack(pady=(0, 8))

    # start background thread (IMPORTANT FIX)
    thread = threading.Thread(
        target=_background_fetch,
        args=(label, root),
        daemon=True
    )
    thread.start()

    return label