Distance & Retailer Mapping Platform

An internal store-location and distance engine built without Google Maps API.

This system enables radius-based store lookup using a custom Haversine distance implementation and optimized database filtering.

Features

Store ingestion system
Multi-retailer data model
Haversine distance calculation
Radius filtering
Bounding box performance optimization
Indexed geospatial queries
Clean REST API endpoint
Zero third-party API cost

API Endpoint
GET /stores?zip=90210&radius=10

Response:

{
  "zip": "90210",
  "radius_miles": 10,
  "stores": [
    {
      "store_name": "...",
      "address": "...",
      "distance_miles": 2.4
    }
  ]
}

Architecture Summary

FastAPI backend
PostgreSQL database
SQLAlchemy ORM
Bounding box + Haversine filtering
Indexed lat/lon columns