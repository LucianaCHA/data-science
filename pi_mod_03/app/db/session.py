from app.config.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = Settings().DB_URL


engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    print("Obteniendo sesión de base de datos...", DATABASE_URL)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
