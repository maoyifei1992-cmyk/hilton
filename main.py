from flask import Flask, Response
import requests
import json
import datetime

app = Flask(__name__)

# Hilton brand codes
BRANDS = [
    "HI", "DT", "WA", "XR", "CN", "CQ", "TC", "CP",
    "EM", "HM", "H2", "HG", "HP", "SI", "MO", "TE", "TR", "HO"
]

API_URL = "https://www.hilton.com/en/locations/api/locations"
HEADERS = {"User-Agent": "Mozilla/5.0"}
HOTEL_FILE = "hotels.json"


def update_hotels():
    """Fetch all Hilton hotels and save to hotels.json"""
    hotels = []
    for brand in BRANDS:
        try:
            params = {"brandCode": brand, "pageSize": 2000}
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

    # Save to JSON
    with open(HOTEL_FILE, "w", encoding="utf-8") as f:
        json.dump(hotels, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(hotels)} Hilton hotels worldwide.")


def generate_rss():
    """Generate RSS feed from hotels.json"""
    try:
        with open(HOTEL_FILE, "r", encoding="utf-8") as f:
            hotels = json.load(f)
    except FileNotFoundError:
        hotels = []

    rss_items = ""
    for hotel in hotels[:50]:  # limit to 50 recent items
        rss_items += f"""
        <item>
            <title>{hotel['name']} ({hotel['city']}, {hotel['country']})</title>
            <link>https://www.hilton.com/en/hotels/</link>
            <description>Hilton {hotel['brand']} hotel in {hotel['city']}, {hotel['country']}</description>
            <pubDate>{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Hilton Hotels</title>
        <description>Latest Hilton hotels worldwide</description>
        <link>https://your-app.up.railway.app/rss</link>
        {rss_items}
      </channel>
    </rss>"""
    return rss_feed


@app.route("/update")
def update():
    """Manual trigger to fetch Hilton hotels"""
    update_hotels()
    return "Hotels updated!"


@app.route("/rss")
def rss():
    """Serve RSS feed"""
    return Response(generate_rss(), mimetype="application/rss+xml")


if __name__ == "__main__":
    # Optional: update hotels on start
    update_hotels()
    app.run(host="0.0.0.0", port=8080)
