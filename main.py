import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from py_pushover_client import PushoverAPIClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from database.models import ScrapedData, ScrapeTargets
from tools.functions import write_file
from tools.scraper import ScraperException, get_scraper

LOGS_DIR = Path(__file__).parent / "logs"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=LOGS_DIR / "frog.log",
)


load_dotenv()
API_TOKEN = os.getenv("NOTIFICATION_TOKEN")
USER_KEY = os.getenv("NOTIFICATION_USER_KEY")
notification = PushoverAPIClient(api_token=API_TOKEN, user_key=USER_KEY)

session = Session(engine)
stmt = select(ScrapeTargets)
products = session.scalars(stmt)


for product in products:
    try:
        logging.info(f"Getting data for '{product.sku}'")
        scraper = get_scraper(product.site, product.sku)

        if scraper.run():
            price = scraper.get_price()
            title = scraper.get_title()
            # get current time in UTC but remove timezone info so it can be stored in sqlite
            # this is different from datetime.now() which returns local time (not UTC)
            timestamp = datetime.now(timezone.utc).replace(tzinfo=None)

            # save data to database and send notification if needed
            product.scraped_data.append(
                ScrapedData(
                    timestamp=timestamp,
                    price=price,
                    title=title,
                )
            )
            product.last_scraped = timestamp
            session.add(product)
            session.commit()

            if product.send_notification:
                notification.send(title=title, message=price)
                logging.info(f"Sent notification for '{product.sku}'")
        else:
            logging.warning(f"Could not find price and title for '{product.sku}'")
            # error getting data so we save the raw html for debugging
            write_file(
                dir=LOGS_DIR / "html_logs",
                filename=f"{product.sku}.html",
                content=str(scraper.get_html()),
            )
    except ScraperException as e:
        logging.error(f"Scraper failure: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    # Sleep for 1 second to avoid getting blocked
    time.sleep(1)
