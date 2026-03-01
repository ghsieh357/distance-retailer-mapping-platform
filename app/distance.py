"""
Distance calculation utilities.
Implements Haversine formula and filtering logic.
"""

import math
from typing import List, Dict


EARTH_RADIUS_MILES = 3958.8


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates in miles.
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_MILES * c


def filter_and_sort_stores(
    origin_lat: float,
    origin_lon: float,
    stores: List[Dict],
    radius_miles: float,
) -> List[Dict]:
    """
    Filter stores within radius and sort by distance.
    """
    results = []

    for store in stores:
        distance = haversine_distance(
            origin_lat,
            origin_lon,
            store["lat"],
            store["lon"],
        )

        if distance <= radius_miles:
            store_copy = store.copy()
            store_copy["distance_miles"] = round(distance, 2)
            results.append(store_copy)

    results.sort(key=lambda x: x["distance_miles"])
    return results

def calculate_bounding_box(lat: float, lon: float, radius_miles: float):
    """
    Calculate bounding box around a point.
    Returns (min_lat, max_lat, min_lon, max_lon).
    """
    lat_delta = radius_miles / 69.0
    lon_delta = radius_miles / (69.0 * math.cos(math.radians(lat)))

    min_lat = lat - lat_delta
    max_lat = lat + lat_delta
    min_lon = lon - lon_delta
    max_lon = lon + lon_delta

    return min_lat, max_lat, min_lon, max_lon