"""
Basic FastAPI application for DB connection test.
"""

from fastapi import FastAPI, HTTPException, Depends
from .zipcodes import ZIP_CODE_COORDS
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_db, engine
from . import models
from .distance import filter_and_sort_stores
from .distance import calculate_bounding_box

app = FastAPI()


@app.get("/")
def health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"status": "ok", "db_check": result.scalar()}
    

@app.get("/stores")
def get_stores_by_zip(
    zip: str,
    radius: float = 10,
    db: Session = Depends(get_db),
):
    if zip not in ZIP_CODE_COORDS:
        raise HTTPException(status_code=404, detail="ZIP code not supported")

    origin = ZIP_CODE_COORDS[zip]

    min_lat, max_lat, min_lon, max_lon = calculate_bounding_box(
    origin["lat"],
    origin["lon"],
    radius,
)

    stores = (
        db.query(models.Store)
        .filter(models.Store.lat.between(min_lat, max_lat))
        .filter(models.Store.lon.between(min_lon, max_lon))
        .all()
    )

    store_dicts = [
        {
            "store_name": s.store_name,
            "address": s.address,
            "lat": s.lat,
            "lon": s.lon,
        }
        for s in stores
    ]

    filtered = filter_and_sort_stores(
        origin["lat"],
        origin["lon"],
        store_dicts,
        radius,
    )

    response_stores = [
        {
            "store_name": s["store_name"],
            "address": s["address"],
            "distance_miles": s["distance_miles"],
        }
        for s in filtered
    ]

    return {
        "zip": zip,
        "radius_miles": radius,
        "stores": response_stores,
    }