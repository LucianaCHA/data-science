import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Leer config de conexión
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Crear string de conexión
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Crear engine y sesión
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Metadata para definir tablas (si no tienes modelos declarativos)
metadata = MetaData()

Usuarios = Table('Usuarios', metadata,
    Column('UsuarioID', Integer, primary_key=True),
    Column('Nombre', String),
    Column('Apellido', String),
    Column('DNI', String),
    Column('Email', String),
    Column('Contraseña', String),
    # más columnas según definición
)

def populate():
    # Ejemplo insert simple
    session.execute(
        Usuarios.insert(),
        [
            {'Nombre': 'Encarna', 'Apellido': 'Donaire', 'DNI': '49877134', 'Email': 'encarna.donaire1@correo.com', 'Contraseña': 'Contraseña123'},
            {'Nombre': 'Jose Ignacio', 'Apellido': 'Canales', 'DNI': '98778810', 'Email': 'jose ignacio.canales2@correo.com', 'Contraseña': 'Contraseña123'},
        ]
    )
    session.commit()
    print("Datos insertados correctamente.")

if __name__ == "__main__":
    populate()
