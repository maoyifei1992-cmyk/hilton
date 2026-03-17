import smtplib
import time
import random
import requests

EMAIL = "yifei589@gmail.com"
PASSWORD = "your_app_password"
TO_EMAIL = "yifei589@gmail.com"

# Sample hotels (you can expand later)
HOTELS = [
    {"name": "Conrad Tokyo", "avg_price": 400},
    {"name": "Waldorf Astoria Shanghai", "avg_price": 350},
    {"name": "Hilton London Metropole", "avg_price": 250},
]

sent_alerts = set()

def get_price(hotel):
    # ⚠️ TEMP: replace with real scraping/API later
    return random.randint(80, 500)


SENDGRID_API_KEY = "your_sendgrid_api_key"

def send_email(hotel, price):
    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "personalizations": [
            {
                "to": [{"email": "your@gmail.com"}],
                "subject": f"🔥 Hilton Bug Price: {hotel['name']}"
            }
        ],
        "from": {"email": "your@gmail.com"},
        "content": [
            {
                "type": "text/plain",
                "value": f"""
Hotel: {hotel['name']}
Normal: ${hotel['avg_price']}
Now: ${price}

<50% DEAL DETECTED — BOOK NOW
"""
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)

def check_prices():
    for hotel in HOTELS:
        price = get_price(hotel)

        if price < hotel["avg_price"] * 0.5:
            key = f"{hotel['name']}_{price}"
            if key not in sent_alerts:
                send_email(hotel, price)
                sent_alerts.add(key)
                print(f"ALERT: {hotel['name']} ${price}")

while True:
    check_prices()
    time.sleep(60)
