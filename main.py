import json
import time
import os
from pathlib import Path
from py_pushover_client import PushoverAPIClient
from dotenv import load_dotenv
from tools import Database, get_scraper


load_dotenv()
API_TOKEN = os.getenv("NOTIFICATION_TOKEN")
USER_KEY = os.getenv("NOTIFICATION_USER_KEY")
notification = PushoverAPIClient(api_token=API_TOKEN, user_key=USER_KEY)
scraping_data = Path(__file__).resolve().parent / "data/scraping_data.json"
db = Database()


with scraping_data.open() as f:
    products = json.load(f)

for product in products:
    scraper = get_scraper(product["site"], product["id"])
    price = scraper.get_price()
    title = scraper.get_title()

    db.add_record(title, price)

    if product["notification"]:
        notification.send(title=title, message=price)

    print(f"Added '{title}' with price {price}")

    # Sleep for 5 seconds to avoid getting blocked
    time.sleep(5)
