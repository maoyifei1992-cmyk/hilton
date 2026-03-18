import requests
import json

# Hilton brand codes
BRANDS = [
    "HI", "DT", "WA", "XR", "CN", "CQ", "TC", "CP",
    "EM", "HM", "H2", "HG", "HP", "SI", "MO", "TE", "TR", "HO"
]

API_URL = "https://www.hilton.com/en/locations/api/locations"
HEADERS = {"User-Agent": "Mozilla/5.0"}
JSON_FILE = "hotels.json"

def load_existing_hotels():
    """Load hotels.json if exists, otherwise return empty list."""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            hotels = json.load(f)
            print(f"Loaded {len(hotels)} hotels from file.")
            return hotels
    except FileNotFoundError:
        return []

def save_hotels(hotels):
    """Save hotels list to hotels.json"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(hotels, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(hotels)} hotels to file.")

def fetch_all_hotels():
    """Fetch all Hilton hotels from API and update hotels.json"""
    hotels = load_existing_hotels()
    existing_names = {h["name"] for h in hotels}

    for brand in BRANDS:
        print(f"Fetching brand: {brand}")
        params = {"brandCode": brand, "pageSize": 2000}  # large page to get all
        try:
            r = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
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

    save_hotels(hotels)
    print("Done fetching all hotels.")

if __name__ == "__main__":
    fetch_all_hotels()
