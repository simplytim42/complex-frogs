import json
import time
from tools.notifications import PushNotification
from tools.db import Database
from tools.scraper import Scraper

notification = PushNotification()
db = Database()


with open("data/scraping_data.json") as f:
    products = json.load(f)

for product in products:
    scraper = Scraper(product["url"])
    price = scraper.get_value(product["css_selector"])

    db.add_record(product["title"], price)

    if product["notification"]:
        notification.send(product["title"], price)

    print(f"Added '{product['title']}' with price {price}")
    # Sleep for 5 seconds to avoid getting blocked
    time.sleep(5)
