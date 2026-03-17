import smtplib
import time
import random

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

def send_email(hotel, price):
    subject = f"🔥 Hilton Bug Price: {hotel['name']}"
    body = f"""
Hotel: {hotel['name']}
Normal: ${hotel['avg_price']}
Now: ${price}

<50% DEAL DETECTED — BOOK NOW
"""

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, message)

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
