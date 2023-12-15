"""Test data"""

from datetime import datetime, timezone

timestamp = datetime.now(tz=timezone.utc)

scrape_target1 = {
    "site": "test site1",
    "sku": "test sku1",
    "send_notification": True,
}

scrape_target2 = {
    "site": "test site2",
    "sku": "test sku2",
    "send_notification": True,
}

scraped_data1 = {
    "scrape_target_id": 1,
    "title": "test title1",
    "price": "£10",
}
