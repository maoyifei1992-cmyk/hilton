import requests
import json
import random
from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)

API_URL = "https://www.hilton.com/en/locations/api/locations"
BRANDS = [
    "HI", "DT", "WA", "XR", "CN", "CQ", "TC", "CP",
    "EM", "HM", "H2", "HG", "HP", "SI", "MO", "TE", "TR", "HO"
]
JSON_FILE = "hotels.json"

def fetch_hotels():
    """Fetch Hilton hotels and update hotels.json with new entries."""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except FileNotFoundError:
        hotels = []

    existing_names = {h["name"] for h in hotels}

    for brand in BRANDS:
        try:
            r = requests.get(API_URL, params={"brandCode": brand, "pageSize": 2000}, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            data = r.json()
            for item in data.get("locations", []):
                name = item.get("name")
                city = item.get("address", {}).get("city")
                country = item.get("address", {}).get("country")
                if name and city and country and name not in existing_names:
                    hotels.append({
                        "name": name,
                        "city": city,
                        "country": country,
                        "brand": brand
                    })
                    existing_names.add(name)
        except Exception as e:
            print(f"Error fetching {brand}: {e}")

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(hotels, f, indent=2, ensure_ascii=False)

    print(f"Loaded {len(hotels)} hotels in total.")
    return hotels

def generate_rss(hotels):
    """Generate RSS feed with simulated bug prices (<50%)."""
    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []

    for hotel in hotels:
        # simulate random bug price between 20%-49%
        bug_price = random.randint(20, 49)
        title = f"{hotel['name']} ({hotel['city']}, {hotel['country']}) - Bug price {bug_price}% OFF!"
        description = f"Hilton {hotel['brand']} hotel in {hotel['city']}, {hotel['country']}. Discount: {bug_price}%"
        link = "https://www.hilton.com/en/hotels/"
        item = f"""
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <description>{description}</description>
            <pubDate>{now}</pubDate>
        </item>
        """
        items.append(item.strip())

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Hilton Bug Price Alerts</title>
    <description>Real-time bug price alerts (&lt;50%)</description>
    <link>https://your-app.up.railway.app/rss</link>
    {"".join(items)}
  </channel>
</rss>
"""
    return rss_feed

@app.route("/rss")
def rss():
    hotels = fetch_hotels()
    feed = generate_rss(hotels[:50])  # limit to 50 items to avoid huge feed
    return Response(feed, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
