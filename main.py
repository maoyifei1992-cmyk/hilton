import json
import random
import time
from flask import Flask, Response

# ================================
# Use Railway persistent storage
# Make sure you mounted a volume, e.g., /data
HOTEL_FILE = "/data/hotels.json"
app = Flask(__name__)

# ================================
# Load hotels from JSON
def load_hotels():
    try:
        with open(HOTEL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Initialize empty if file doesn't exist
        return []

# Save hotels back to JSON
def save_hotels(hotels):
    with open(HOTEL_FILE, "w", encoding="utf-8") as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

# ================================
# Generate RSS feed
def generate_rss():
    hotels = load_hotels()

    rss_items = ""
    for hotel in hotels:
        rss_items += f"""
        <item>
            <title>{hotel['name']} - {hotel['price_drop']}% Off</title>
            <link>{hotel['link']}</link>
            <description>Price dropped by {hotel['price_drop']}%</description>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Hilton Bug Price Alerts</title>
    <description>Real-time bug price alerts (&lt;50%)</description>
    <link>https://your-app.up.railway.app/rss</link>
    {rss_items}
  </channel>
</rss>"""
    return rss_feed

# ================================
# Routes
@app.route("/")
def home():
    return "<h1>Hilton Bug Price Alerts</h1><p>Go to <a href='/rss'>/rss</a> for feed.</p>"

@app.route("/rss")
def rss():
    # simulate delay for scraping (optional)
    time.sleep(random.randint(1, 3))
    feed = generate_rss()
    return Response(feed, mimetype="application/rss+xml")

# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
