from flask import Flask, jsonify, Response
import requests
import json

app = Flask(__name__)

# Hilton brand codes (you can expand if needed)
BRANDS = ["HI","DT","WA","XR","CN","CQ","TC","CP","EM","HM","H2","HG","HP","SI","MO","TE","TR","HO"]

def fetch_hotels():
    hotels = []
    for brand in BRANDS:
        try:
            # Hilton API for locations
            r = requests.get(
                "https://www.hilton.com/en/locations/api/locations",
                params={"brandCode": brand, "pageSize": 2000},
                timeout=10
            )
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
    return hotels

@app.route("/hotels.json")
def hotels_json():
    hotels = fetch_hotels()
    return jsonify(hotels)

@app.route("/hotels.txt")
def hotels_txt():
    hotels = fetch_hotels()
    content = "\n".join([f"{h['name']} - {h['city']}, {h['country']} ({h['brand']})" for h in hotels])
    return Response(content, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
