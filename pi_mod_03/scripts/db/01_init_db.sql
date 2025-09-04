CREATE TABLE IF NOT EXISTS airbnb_raw (
    id INTEGER PRIMARY KEY,
    name TEXT,
    host_id INTEGER,
    host_name TEXT,
    neighbourhood_group TEXT,
    neighbourhood TEXT,
    latitude FLOAT,
    longitude FLOAT,
    room_type TEXT,
    price INTEGER,
    minimum_nights INTEGER,
    number_of_reviews INTEGER,
    last_review DATE,
    reviews_per_month FLOAT,
    calculated_host_listings_count INTEGER,
    availability_365 INTEGER
);
