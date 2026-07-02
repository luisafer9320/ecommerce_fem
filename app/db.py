"""
Módulo de conexión a la base de datos SQLite.
Usa SQLAlchemy con sesiones sincrónicas.

Qué es esto?
- SQLite: Base de datos ligera (archivo .db)
- SQLAlchemy: Librería que permite trabajar con BD sin escribir SQL directo
- Sesiones: Conexiones a la BD que se abren y cierran
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Cargar variables de entorno desde archivo .env
load_dotenv()

# ============================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================
# Obtiene la URL de la BD de variables de entorno
# Si no existe, usa SQLite en un archivo local
database_url = os.getenv("DATABASE_URL", "sqlite:///./clinica_veterinaria.db")

# ============================================
# CREAR EL "MOTOR" O CONEXIÓN PRINCIPAL
# ============================================
# engine: Objeto que gestiona todas las conexiones a la BD
# echo=True: Muestra todas las sentencias SQL en consola (útil para debug)
engine = create_engine(database_url, echo=True)

# ============================================
# CONFIGURAR SESIONES
# ============================================
# Una sesión es como "abrir una conversación" con la BD
# Configuración:
#   - autocommit=False: Los cambios NO se guardan automáticamente
#                       Deben hacerlo con commit() explícitamente
#   - autoflush=False: Los cambios NO se sincronizan automáticamente
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================
# BASE PARA TODOS LOS MODELOS
# ============================================
# DeclarativeBase: Clase base que SQLAlchemy usa para crear modelos
# Todos los modelos de datos heredan de esta clase "Base"
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

