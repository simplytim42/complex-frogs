import json
import time
import os
from py_pushover_client import PushoverAPIClient
from tools.db import Database
from tools.scraper import Scraper
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv("NOTIFICATION_TOKEN")
USER_KEY = os.getenv("NOTIFICATION_USER_KEY")
notification = PushoverAPIClient(api_token=API_TOKEN, user_key=USER_KEY)
db = Database()


with open("data/scraping_data.json") as f:
    products = json.load(f)


for product in products:
    scraper = Scraper(product["url"])
    price = scraper.get_value(product["css_selector"])

    db.add_record(product["title"], price)

    if product["notification"]:
        notification.send(title=product["title"], message=price)

    print(f"Added '{product['title']}' with price {price}")

    # Sleep for 5 seconds to avoid getting blocked
    time.sleep(5)
