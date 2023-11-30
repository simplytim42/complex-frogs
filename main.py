# standard library imports
import time
from datetime import datetime
import os
import logging
from pathlib import Path

# third party imports
from py_pushover_client import PushoverAPIClient
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import select

# local imports
from tools.scraper.scraper_dispatcher import get_scraper
from tools.scraper.base_scraper import ScraperException
from tools.functions import write_file
from database import engine
from database.models import ScrapeTargets, ScrapedData

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

            # save data to database and send notification if needed
            product.scraped_data.append(
                ScrapedData(
                    timestamp=datetime.now(),
                    price=price,
                    title=title,
                )
            )
            product.last_scraped = datetime.now()
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
