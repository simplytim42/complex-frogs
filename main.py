import json
import time
import datetime
import os
import logging
from pathlib import Path
from py_pushover_client import PushoverAPIClient
from dotenv import load_dotenv
from tools.database import Database
from tools.scraper.scraper_dispatcher import get_scraper


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="frog.log",
)


load_dotenv()
API_TOKEN = os.getenv("NOTIFICATION_TOKEN")
USER_KEY = os.getenv("NOTIFICATION_USER_KEY")
notification = PushoverAPIClient(api_token=API_TOKEN, user_key=USER_KEY)
scraping_data = Path(__file__).resolve().parent / "data/scraping_data.json"
db = Database()


with scraping_data.open() as f:
    products = json.load(f)


for product in products:
    try:
        logging.info(f"Getting data for '{product['id']}'")
        scraper = get_scraper(product["site"], product["id"])

        if scraper.run():
            price = scraper.get_price()
            title = scraper.get_title()

            # save data to database and send notification if needed
            db.add_record(title, price)

            if product["notification"]:
                notification.send(title=title, message=price)
                logging.info(f"Sent notification for '{product['id']}'")
        else:
            logging.info(f"Could not find price and title for '{product['id']}'")
            # error getting data so we save the raw html for debugging
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"html_logs/{timestamp}_{product['id']}.html"
            with Path(__file__).resolve().parent / filename as f:
                f.parent.mkdir(parents=True, exist_ok=True)
                html = str(scraper.get_html())
                f.write_text(html)

    except Exception as e:
        logging.error(f"Failed to get data: {e}")

    # Sleep for 5 seconds to avoid getting blocked
    time.sleep(1)
