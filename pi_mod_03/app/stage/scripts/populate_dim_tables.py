from sqlalchemy import create_engine, text
import logging
from app.config import config
from app.services.logger.gcloud_logger import CloudLogger

# Configuración de logger
logger = CloudLogger()
settings = config.Settings()


def create_rooms_dim_table(engine):
    logger.info("Creating 'rooms_dim' table if not exists...")

    create_sql = """
    CREATE TABLE IF NOT EXISTS rooms_dim (
        id SERIAL PRIMARY KEY,
        host_id INTEGER,
        neighbourhood_group TEXT,
        neighbourhood TEXT,
        room_type TEXT,
        price INTEGER,
        minimum_nights INTEGER,
        number_of_reviews INTEGER,
        last_review DATE,
        reviews_per_month FLOAT,
        calculated_host_listings_count INTEGER,
        availability_365 INTEGER
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_sql))

    logger.info("'rooms_dim' table created or already exists.")


def populate_rooms_dim(engine):
    logger.info("Populating 'rooms_dim' table...")

    insert_sql = """
    INSERT INTO rooms_dim (
        host_id, neighbourhood_group, neighbourhood, room_type,
        price, minimum_nights, number_of_reviews, last_review,
        reviews_per_month, calculated_host_listings_count, availability_365
    )
    SELECT
        host_id,
        neighbourhood_group,
        neighbourhood,
        room_type,
        price,
        minimum_nights,
        number_of_reviews,
        last_review,
        reviews_per_month,
        calculated_host_listings_count,
        availability_365
    FROM airbnb_raw;
    """

    with engine.connect() as conn:
        conn.execute(text(insert_sql))

    logger.info("'rooms_dim' table populated successfully.")


def populate_dim_tables():
    logger.info("Creating and populating dimension table 'rooms_dim'...")
    db_url = settings.DB_URL
    engine = create_engine(db_url)

    create_rooms_dim_table(engine)
    populate_rooms_dim(engine)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    populate_dim_tables()
