"""
Punto de entrada de la aplicación FastAPI.
Configuración de routers y eventos de startup.

Este es el archivo principal que:
1. Crea la aplicación FastAPI
2. Inicializa la base de datos
3. Registra todos los routers (rutas) de la aplicación
"""
from fastapi import FastAPI

from app.db import initialize_db
from app.routers.router_home import router as home_router
from app.routers.router_mascotas import router as mascotas_router
from app.routers.router_propietarios import router as propietarios_router

# ============================================
# CREAR LA APLICACIÓN FastAPI
# ============================================
# FastAPI es un framework moderno para crear APIs REST
# Parámetros:
#   - title: Nombre de la API
#   - version: Versión de la API
#   - description: Descripción de qué hace la API
#   - docs_url: URL para ver documentación interactiva (Swagger)
#   - redoc_url: URL para documentación alternativa (ReDoc)
app = FastAPI(
    title="Clinica_Veterinaria",
    version="1.0.0",
    description="API Clinica Veterinaria FemCoders",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================
# INICIALIZAR LA BASE DE DATOS
# ============================================
# Esta función crea las tablas en la BD si no existen
initialize_db()

# ============================================
# REGISTRAR ROUTERS (Rutas de la API)
# ============================================
# Los routers son grupos de endpoints organizados por tema
# Cada router maneja un recurso diferente:
#   - home_router: Página principal
#   - propietarios_router: Operaciones con propietarios
#   - mascotas_router: Operaciones con mascotas
app.include_router(home_router, tags=["Home"])
app.include_router(propietarios_router)
app.include_router(mascotas_router)



