# main.py
from flask import Flask, Response
import datetime
import json
import os

app = Flask(__name__)

# Path to your hotels.json file
HOTELS_FILE = os.path.join(os.path.dirname(__file__), "hotels.json")

def load_hotels():
    """Load hotel data from JSON file"""
    try:
        with open(HOTELS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading hotels.json: {e}")
        return []

def generate_rss():
    """Generate RSS feed XML from hotel data"""
    hotels = load_hotels()
    items_xml = ""
    for hotel in hotels:
        items_xml += f"""
        <item>
            <title>{hotel.get('name', 'Unknown Hotel')} Price Drop!</title>
            <description>{hotel.get('price_drop', '?')}% off</description>
            <link>{hotel.get('link', '#')}</link>
            <pubDate>{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
        </item>
        """

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Hilton Bug Price Alerts</title>
        <description>Real-time bug price alerts (&lt;50%)</description>
        <link>https://your-app.up.railway.app/rss</link>
        {items_xml}
      </channel>
    </rss>"""
    return rss_xml

@app.route("/rss")
def rss():
    rss_feed = generate_rss()
    return Response(rss_feed, mimetype="application/rss+xml")

@app.route("/")
def home():
    return "Hilton Bug Price Alerts API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
