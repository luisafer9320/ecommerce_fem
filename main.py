"""
Punto de entrada de la aplicación FastAPI.
Configuración de routers y eventos de startup.
"""
from fastapi import FastAPI
from app.db import engine, Base
from app.routers.router_home import router as home_router
from app.routers.router_razas import router as razas_router
from app.routers.router_propietarios import router as propietarios_router
from app.routers.router_mascotas import router as mascotas_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="Clinica_Veterinaria",
    version="1.0.0",
    description="API Clinica Veterinaria FemCoders",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Crear tablas en la base de datos al iniciar la aplicación
Base.metadata.create_all(bind=engine)

# Registrar routers
app.include_router(home_router, tags=["Home"])
app.include_router(razas_router)
app.include_router(propietarios_router)
app.include_router(mascotas_router)



