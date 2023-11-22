#  THIS FILE IS TEMPORARY AND IS ONLY USED TO UPGRADE THE PROD DB FROM
#  A FILE DB TO A SQLITE DB. THIS FILE WILL BE DELETED ONCE THE DB IS
#  UPGRADED.

from datetime import datetime
from pathlib import Path
import json

from sqlalchemy.orm import Session

from database import engine
from database.models import Base, ScrapeTargets


scraping_data = Path(__file__).resolve().parent / "data/scraping_data.json"
with scraping_data.open() as f:
    products = json.load(f)

#  CREATE TABLES
Base.metadata.create_all(engine)


# ADD DATA
with Session(engine) as session:
    targets = []

    for product in products:
        targets.append(
            ScrapeTargets(
                site=product["site"],
                sku=product["id"],
                send_notification=product["notification"],
                date_added=datetime.now(),
            )
        )

    session.add_all([*targets])
    session.commit()
