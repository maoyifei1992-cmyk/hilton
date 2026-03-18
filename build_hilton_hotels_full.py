import requests
import json

# All known Hilton brand codes
BRANDS = [
    "HI", "DT", "WA", "XR", "CN", "CQ", "TC", "CP",
    "EM", "HM", "H2", "HG", "HP", "SI", "MO", "TE", "TR", "HO"
]

API_URL = "https://www.hilton.com/en/locations/api/locations"
HEADERS = {"User-Agent": "Mozilla/5.0"}

hotels = []

for brand in BRANDS:
    print(f"Fetching brand: {brand}")
    params = {"brandCode": brand, "pageSize": 2000}  # large page to get all hotels
    
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

# Save all hotels
with open("hotels.json", "w", encoding="utf-8") as f:
    json.dump(hotels, f, indent=2, ensure_ascii=False)

print(f"Generated {len(hotels)} Hilton hotels worldwide.")
