import requests
import json
import random
import time
from datetime import datetime
from flask import Flask, Response
import html  # for XML escaping

app = Flask(__name__)

# Hilton brand codes
BRANDS = [
    "HI", "DT", "WA", "XR", "CN", "CQ", "TC", "CP",
    "EM", "HM", "H2", "HG", "HP", "SI", "MO", "TE", "TR", "HO"
]

API_URL = "https://www.hilton.com/en/locations/api/locations"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Load or fetch hotels
def load_hotels():
    try:
        with open("hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)
            print(f"Loaded {len(hotels)} hotels from file.")
            return hotels
    except FileNotFoundError:
        print("hotels.json not found. Fetching from API...")
        hotels = []
        for brand in BRANDS:
            print(f"Fetching brand: {brand}")
            params = {"brandCode": brand, "pageSize": 2000}
            try:
                r = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
                data = r.json()
                for item in data.get("locations", []):
                    name = item.get("name")
                    city = item.get("address", {}).get("city")
                    country = item.get("address", {}).get("country")
                    if name and city and country:
                        hotels.append({
                            "name": name,
                            "city": city,
                            "country": country,
                            "brand": brand
                        })
            except Exception as e:
                print(f"Error fetching {brand}: {e}")
        # Save for next time
        with open("hotels.json", "w", encoding="utf-8") as f:
            json.dump(hotels, f, indent=2, ensure_ascii=False)
        print(f"Generated {len(hotels)} Hilton hotels worldwide.")
        return hotels

hotels = load_hotels()

# Simulate bug prices (<50% discount)
def simulate_bug_prices():
    updated = []
    for h in hotels:
        # Randomly select some hotels for bug prices
        if random.random() < 0.05:  # 5% of hotels
            current_price = round(random.uniform(80, 300), 2)
            discount = random.uniform(0.5, 0.9)  # 50%-90% off
            h_copy = h.copy()
            h_copy["current_price"] = current_price
            h_copy["discount"] = discount
            h_copy["url"] = f"https://www.hilton.com/en/hotels/"  # placeholder
            updated.append(h_copy)
    return updated

# Generate RSS XML
def generate_rss():
    bug_hotels = simulate_bug_prices()
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '<channel>',
        '<title>Hilton Bug Price Alerts</title>',
        '<description>Real-time bug price alerts (&lt;50%)</description>',
        '<link>https://your-app.up.railway.app/rss</link>'
    ]
    for h in bug_hotels:
        rss.append("<item>")
        rss.append(f"<title>{html.escape(h['name'])} ({html.escape(h['city'])}, {html.escape(h['country'])})</title>")
        rss.append(f"<link>{h['url']}</link>")
        rss.append(
            f"<description>Hilton {html.escape(h['brand'])} hotel in {html.escape(h['city'])}, "
            f"{html.escape(h['country'])}. Price: ${h['current_price']} ({int(h['discount']*100)}% off)</description>"
        )
        rss.append(f"<pubDate>{now}</pubDate>")
        rss.append("</item>")
    rss.append("</channel>")
    rss.append("</rss>")
    return "\n".join(rss)

@app.route("/rss")
def rss_feed():
    xml = generate_rss()
    return Response(xml, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
