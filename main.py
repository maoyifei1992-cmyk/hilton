import time
import random
from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)

# In-memory RSS items
rss_items = []

HOTELS = [
    {"name": "Conrad Tokyo", "avg_price": 400},
    {"name": "Waldorf Astoria Shanghai", "avg_price": 350},
    {"name": "Hilton London Metropole", "avg_price": 250},
]

def get_price(hotel):
    # ⚠️ Replace later with real Hilton data
    return random.randint(80, 500)

def add_rss_item(hotel, price):
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    item = f"""
    <item>
      <title>🔥 Hilton Bug Price: {hotel['name']}</title>
      <description>
        Normal: ${hotel['avg_price']} | Now: ${price}
        (&lt;50% DEAL DETECTED)
      </description>
      <pubDate>{now}</pubDate>
      <guid>{hotel['name']}-{price}-{now}</guid>
    </item>
    """

    rss_items.insert(0, item)

    # Keep last 50 alerts only
    if len(rss_items) > 50:
        rss_items.pop()

def generate_rss():
    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Hilton Bug Price Alerts</title>
        <description>Real-time bug price alerts (&lt;50%)</description>
        <link>https://your-app.up.railway.app/rss</link>
        {''.join(rss_items)}
      </channel>
    </rss>
    """
    return rss_feed

@app.route("/rss")
def rss():
    return Response(generate_rss(), mimetype="application/rss+xml")

def check_prices():
    for hotel in HOTELS:
        price = get_price(hotel)

        if price < hotel["avg_price"] * 0.5:
            add_rss_item(hotel, price)
            print(f"ALERT: {hotel['name']} ${price}")

# Background loop
def run_checker():
    while True:
        check_prices()
        time.sleep(60)

# Start background thread
import threading
threading.Thread(target=run_checker, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
