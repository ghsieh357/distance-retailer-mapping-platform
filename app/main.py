"""
Basic FastAPI application for DB connection test.
"""

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db
from .database import engine
from . import models
from .distance import filter_and_sort_stores


app = FastAPI()


@app.get("/")
def health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"status": "ok", "db_check": result.scalar()}
    
@app.get("/test-distance")
def test_distance(
    lat: float,
    lon: float,
    radius: float = 10,
    db: Session = Depends(get_db),
):
    stores = db.query(models.Store).all()

    store_dicts = [
        {
            "store_name": s.store_name,
            "address": s.address,
            "lat": s.lat,
            "lon": s.lon,
        }
        for s in stores
    ]

    results = filter_and_sort_stores(lat, lon, store_dicts, radius)

    return {
        "origin": {"lat": lat, "lon": lon},
        "radius_miles": radius,
        "results": results,
    }