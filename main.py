import json
from tools.notifications import PushNotification
from tools.db import FileDatabase
from tools.scraper import Scraper

notification = PushNotification()
db = FileDatabase()


with open("data/scraping_data.json") as f:
    products = json.load(f)

for product in products:
    scraper = Scraper(product["url"])
    price = scraper.get_value(product["css_selector"])

    db.write_line(product["title"], price)

    if product["notification"]:
        notification.send(product["title"], price)
