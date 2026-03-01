"""
Store ingestion script for Walmart.

This script:
- Ensures retailer exists
- Inserts store records
- Avoids duplicates
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models


WALMART_STORES = [
    {
        "store_name": "Walmart Supercenter Beverly Hills",
        "address": "123 Example St, Beverly Hills, CA 90210",
        "lat": 34.073620,
        "lon": -118.400356,
    },
    {
        "store_name": "Walmart Supercenter Santa Monica",
        "address": "456 Ocean Ave, Santa Monica, CA 90401",
        "lat": 34.019454,
        "lon": -118.491191,
    },
    {
        "store_name": "Walmart Supercenter Westwood",
        "address": "789 Westwood Blvd, Los Angeles, CA 90024",
        "lat": 34.062285,
        "lon": -118.445181,
    },
]


def get_or_create_retailer(db: Session, name: str):
    retailer = db.query(models.Retailer).filter_by(name=name).first()
    if retailer:
        return retailer

    retailer = models.Retailer(name=name)
    db.add(retailer)
    db.commit()
    db.refresh(retailer)
    return retailer


def store_exists(db: Session, store_name: str):
    return db.query(models.Store).filter_by(store_name=store_name).first()


def ingest():
    db = SessionLocal()

    try:
        retailer = get_or_create_retailer(db, "Walmart")

        for store_data in WALMART_STORES:
            if store_exists(db, store_data["store_name"]):
                continue

            store = models.Store(
                store_name=store_data["store_name"],
                address=store_data["address"],
                lat=store_data["lat"],
                lon=store_data["lon"],
                retailer_id=retailer.id,
            )

            db.add(store)

        db.commit()
        print("Ingestion complete.")

    finally:
        db.close()


if __name__ == "__main__":
    ingest()