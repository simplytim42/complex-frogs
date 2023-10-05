import os
import requests
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

response = requests.get(os.getenv("PRODUCT_URL"))
soup = BeautifulSoup(response.text, "html.parser")
product_title = soup.find("span", "product-name").string
price = soup.find("span", "regular-price").string


file_db = Path("products.txt")
date_today = date.today().isoformat()
with file_db.open("a") as f:
    f.write(f"{date_today}|{product_title}|{price}\n")


NOTIFICATION_URL = "https://api.pushover.net/1/messages.json"
response = requests.post(
    NOTIFICATION_URL,
    data={
        "token": os.getenv("NOTIFICATION_TOKEN"),
        "user": os.getenv("NOTIFICATION_USER_KEY"),
        "title": product_title,
        "message": price,
        "sound": "pianobar",
    },
)
