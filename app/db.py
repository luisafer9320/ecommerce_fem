"""
Módulo de conexión a la base de datos SQLite.
Usa SQLAlchemy con sesiones sincrónicas.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

database_url = os.getenv("DATABASE_URL", "sqlite:///./clinica_veterinaria.db")

# Crear el motor de conexión principal
# echo=True muestra las queries SQL en la consola (cambiar a False en producción)
engine = create_engine(database_url, echo=True)

# Configurar sesiones locales
# autocommit=False: cambios se guardan solo con commit()
# autoflush=False: cambios no se sincronizarán automáticamente
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    """Base para todos los modelos SQLAlchemy."""
    pass


def initialize_db():
    """Crea las tablas y adapta la base SQLite si detecta un esquema antiguo de mascotas."""
    if str(engine.url).startswith("sqlite"):
        inspector = inspect(engine)
        if inspector.has_table("mascotas"):
            existing_columns = {column["name"] for column in inspector.get_columns("mascotas")}
            if "especie" not in existing_columns or "raza" not in existing_columns or "edad" not in existing_columns or "propietario_id" not in existing_columns or "raza_id" in existing_columns:
                with engine.begin() as connection:
                    connection.execute(text("DROP TABLE mascotas"))

    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependencia FastAPI para inyectar sesiones de BD.
    Abre una conexión, la proporciona, y la cierra después.
    """
    db = SessionLocal()  # Abre la sesión
    try:
        yield db  # Pausa y proporciona la sesión
    finally:
        db.close()  # Cierra la sesión cuando termina

