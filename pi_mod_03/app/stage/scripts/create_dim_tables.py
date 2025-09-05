from app.config import config
from sqlalchemy import create_engine, text
from app.services.logger.gcloud_logger import CloudLogger

logger = CloudLogger()
settings = config.Settings()


def acquire_pg_lock(conn):
    conn.execute(text("SELECT pg_advisory_lock(123456789);"))


def release_pg_lock(conn):
    conn.execute(text("SELECT pg_advisory_unlock(123456789);"))


def create_rooms_dim_table(conn):
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
    conn.execute(text(create_sql))
    logger.info("Tabla 'rooms_dim' creada o ya existente.")


def create_dim_tables():
    logger.info("Intentando crear tabla de dimensión con lock...")
    db_url = settings.DB_URL
    engine = create_engine(db_url)

    with engine.connect() as conn:
        try:
            acquire_pg_lock(conn)
            logger.info("Lock adquirido.")
            create_rooms_dim_table(conn)
            logger.info("Tabla 'rooms_dim' creada exitosamente.")
        except Exception as e:
            logger.error(f"Error creando tabla 'rooms_dim': {e}")
            raise
        finally:
            release_pg_lock(conn)
            logger.info("Lock liberado.")
