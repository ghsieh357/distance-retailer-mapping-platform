"""
Basic FastAPI application for DB connection test.
"""

from fastapi import FastAPI
from sqlalchemy import text

from .database import engine

app = FastAPI()


@app.get("/")
def health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"status": "ok", "db_check": result.scalar()}