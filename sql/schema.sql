CREATE TABLE retailers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    store_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    retailer_id INTEGER REFERENCES retailers(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_stores_lat_lon ON stores(lat, lon);
CREATE INDEX idx_retailer_id ON stores(retailer_id);