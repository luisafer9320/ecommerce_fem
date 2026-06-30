"""
Módulo de conexión a la base de datos SQLite.
Usa SQLAlchemy con sesiones sincrónicas.
"""
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

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

