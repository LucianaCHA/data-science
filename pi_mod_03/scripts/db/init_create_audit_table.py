from sqlalchemy import inspect
from app.db.base import Base
from app.db.session import engine


def create_audit_table():
    inspector = inspect(engine)
    if not inspector.has_table("data_loads_audit"):
        print("Creando tabla de auditoría 'data_loads_audit'...")
        Base.metadata.create_all(bind=engine)
    else:
        print("La tabla 'data_loads_audit' ya existe.")


create_audit_table()
