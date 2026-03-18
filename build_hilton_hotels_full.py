import requests
import json

API_URL = "https://www.hilton.com/en/locations/api/locations"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Hilton Brand Codes — Full Set (approximate list)
BRANDS = [
    "HI",  # Hilton Hotels & Resorts
    "DT",  # DoubleTree by Hilton
    "WA",  # Waldorf Astoria
    "XR",  # LXR Hotels & Resorts
    "CN",  # Conrad Hotels & Resorts
    "CQ",  # Curio Collection
    "TC",  # Tapestry Collection
    "CP",  # Canopy by Hilton
    "GR",  # Graduate Hotels
    "SP",  # Spark by Hilton
    "TE",  # Tempo by Hilton
    "MO",  # Motto by Hilton
    "SI",  # Signia by Hilton
    "EM",  # Embassy Suites
    "HM",  # Homewood Suites
    "H2",  # Home2 Suites
    "HG",  # Hilton Garden Inn
    "HP",  # Hampton by Hilton
    "TR",  # Tru by Hilton
    # Add others if needed
]

hotels = []
seen = set()

for brand in BRANDS:
    print(f"Fetching brand: {brand}")
    params = {"brandCode": brand, "pageSize": 5000}
    try:
        r = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        for item in data.get("locations", []):
            name = item.get("name")
            city = item.get("address", {}).get("city")
            country = item.get("address", {}).get("country")
            if name and city and country:
                key = (name, city, country)
                if key not in seen:
                    seen.add(key)
                    hotels.append({
                        "name": name,
                        "city": city,
                        "country": country,
                        "brand": brand
                    })
    except Exception as e:
        print(f"Error fetching {brand}: {e}")

with open("hotels.json", "w", encoding="utf-8") as f:
    json.dump(hotels, f, indent=2)

print(f"Generated {len(hotels)} Hilton hotels worldwide.")
