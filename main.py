from flask import Flask, Response
import json
import requests
from bs4 import BeautifulSoup
import time
import random

app = Flask(__name__)

# Load Hilton hotels JSON
with open("hotels.json", "r", encoding="utf-8") as f:
    HOTELS = json.load(f)

# Example: simulate average price for bug price calculation
def average_price(hotel):
    # You could fetch this from historical data
    return 200  # placeholder

# OTA scraping function (Booking.com example)
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_price(hotel):
    try:
        query = f"{hotel['name']} {hotel['city']}"
        url = f"https://www.booking.com/searchresults.html?ss={query}"

        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Extract first price found
        price_tags = soup.select('[data-testid="price-and-discounted-price"]')
        for tag in price_tags:
            text = tag.get_text()
            digits = ''.join(filter(str.isdigit, text))
            if digits:
                price = int(digits)
                return price
        return None
    except Exception as e:
        print("OTA fetch error:", e)
        return None

# Generate RSS feed XML
def generate_rss():
    rss_items = ""
    for hotel in HOTELS:
        price = fetch_price(hotel)
        if price and price < 0.5 * average_price(hotel):  # bug price <50%
            rss_items += f"""
            <item>
                <title>{hotel['name']} - ${price}</title>
                <description>Bug price alert: {hotel['name']} in {hotel['city']}, {hotel['country']}</description>
                <link>https://www.hilton.com/en/locations/</link>
            </item>
            """
        # Delay to avoid blocking
        time.sleep(random.randint(2, 5))

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Hilton Bug Price Alerts</title>
        <description>Real-time bug price alerts (<50%)</description>
        <link>https://your-app.up.railway.app/rss</link>
        {rss_items}
      </channel>
    </rss>"""
    return rss_feed

@app.route("/rss")
def rss():
    feed = generate_rss()
    return Response(feed, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
