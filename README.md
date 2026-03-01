# Distance & Retailer Mapping Platform

## Architecture Overview

## Setup Instructions

## API Usage

## Distance Engine

## Performance Strategy
Bounding Box Filtering
To avoid full table scans when computing distances, bounding box is calculated around the origin ZIP using latitude and longitude deltas.

The database query filters stores within:
min_lat ≤ lat ≤ max_lat
min_lon ≤ lon ≤ max_lon

Spatial Indexing
For larger scale (100k+ stores), PostGIS with GiST indexing would eliminate most Python-side filtering. it would allow distance filtering directly in SQL. 

Caching strategy
ZIP-to-coordinate lookups are cached in memory.

At production scale, Redis would cache ZIP → lat/lon, and frequent query results (popular ZIP + radius combos)

Handling 5,000 Concurrent Users

With:
Bounding box filtering
Indexed DB queries
Stateless FastAPI app

System scales horizontally:
Multiple app instances behind load balancer
DB connection pooling
Redis caching layer

## Scale & Cost Strategy
Cheap Store Location Ingestion: 
No per-request API cost if we can use public retailer store locator pages. Just perform one-time ingestion + periodic refresh

Updating Without Constant Scraping
To avoid scraping every day, just run ingestion weekly or monthly via scheduled job
maybe also compare by store_name + address, and insert new stores only

Computing Distances at Scale

Current approach:
Bounding box in SQL
Haversine in Python

At large scale:
Move distance calculation into PostGIS
Use ST_DWithin for radius queries
Use GiST spatial index

Where Caching Should Live

Application Layer:
In-memory LRU for ZIP lookups

Infrastructure Layer:
Redis for ZIP searches/Precomputed radius results

Database Layer:
Indexed columns for efficient filtering

Cost Model

Infrastructure:
Single PostgreSQL instance
FastAPI app server
Optional Redis

No external API usage
## Tradeoffs