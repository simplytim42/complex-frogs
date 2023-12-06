"""Main script to run the scraper and save data to database."""

import logging
import os
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from py_pushover_client import PushoverAPIClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from complex_frogs.database import engine
from complex_frogs.database.models import ScrapedData, ScrapeTargets
from complex_frogs.functions.utils import write_file
from complex_frogs.logger.config import LOGS_DIR, setup_logger
from complex_frogs.scraper import ScraperError, get_scraper

setup_logger(filepath=LOGS_DIR / "frog.log")

load_dotenv()
API_TOKEN = os.getenv("NOTIFICATION_TOKEN")
USER_KEY = os.getenv("NOTIFICATION_USER_KEY")
notification = PushoverAPIClient(api_token=API_TOKEN, user_key=USER_KEY)
session = Session(engine)

stmt = select(ScrapeTargets)
products = session.scalars(stmt)
for product in products:
    try:
        msg = f"Getting data for '{product.sku}'"
        logging.info(msg=msg)
        scraper = get_scraper(site=product.site, product_id=product.sku)

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
                ),
            )
            product.last_scraped = timestamp
            session.add(product)
            session.commit()

            if product.send_notification:
                notification.send(title=title, message=price)
                msg = f"Sent notification for '{product.sku}'"
                logging.info(msg=msg)
        else:
            msg = f"Could not find price and title for '{product.sku}'"
            logging.warning(msg=msg)
            # error getting data so we save the raw html for debugging
            write_file(
                directory=LOGS_DIR / "html_logs",
                filename=f"{product.sku}.html",
                content=str(scraper.get_html()),
            )
    except ScraperError as e:
        msg = f"Scraper failure: {e}"
        logging.exception(msg=msg)
    except Exception as e:
        msg = f"Unexpected error: {e}"
        logging.exception(msg=msg)

    # Sleep for 1 second to avoid getting blocked
    time.sleep(1)
