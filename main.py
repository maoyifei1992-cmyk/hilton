import json
import random
import datetime
from flask import Flask, Response

app = Flask(__name__)

HOTELS_FILE = "hotels.json"

# Load Hilton hotels from hotels.json
def load_hotels():
    try:
        with open(HOTELS_FILE, "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except FileNotFoundError:
        hotels = []
    return hotels

# Simulate fetching current price for each hotel
# Replace this with real price API calls if available
def update_prices(hotels):
    for hotel in hotels:
        normal_price = random.randint(150, 500)  # normal price in USD
        current_price = normal_price * random.uniform(0.3, 1.0)  # simulate discount
        discount = (normal_price - current_price) / normal_price

        hotel["normal_price"] = round(normal_price, 2)
        hotel["current_price"] = round(current_price, 2)
        hotel["discount"] = round(discount, 2)
        hotel["url"] = f"https://www.hilton.com/en/hotels/"  # placeholder URL

    # Save updated hotels back to file
    with open(HOTELS_FILE, "w", encoding="utf-8") as f:
        json.dump(hotels, f, indent=2, ensure_ascii=False)

    return hotels

# Generate RSS feed from hotels with bug prices
def generate_rss(hotels):
    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '<channel>',
        '<title>Hilton Bug Price Alerts</title>',
        '<description>Real-time bug price alerts (<50%)</description>',
        '<link>https://your-app.up.railway.app/rss</link>'
    ]

    for h in hotels:
        if h.get("discount", 0) >= 0.5:  # only bug prices
            rss.append("<item>")
            rss.append(f"<title>{h['name']} ({h['city']}, {h['country']})</title>")
            rss.append(f"<link>{h['url']}</link>")
            rss.append(
                f"<description>Hilton {h['brand']} hotel in {h['city']}, {h['country']}. "
                f"Price: ${h['current_price']} ({int(h['discount']*100)}% off)</description>"
            )
            rss.append(f"<pubDate>{now}</pubDate>")
            rss.append("</item>")

    rss.append("</channel></rss>")
    return "\n".join(rss)

@app.route("/update")
def update_hotels():
    hotels = load_hotels()
    hotels = update_prices(hotels)
    return f"Updated {len(hotels)} hotels with simulated prices."

@app.route("/rss")
def rss_feed():
    hotels = load_hotels()
    return Response(generate_rss(hotels), mimetype="application/xml")

@app.route("/")
def index():
    return "Hilton Bug Price Alerts API. Use /rss for feed, /update to refresh prices."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
