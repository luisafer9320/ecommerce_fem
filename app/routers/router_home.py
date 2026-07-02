"""
Router para la página de inicio de la API.

Este router maneja la raíz (/) de la aplicación.
Es el primer endpoint que se consulta para verificar que la API funciona.
"""
from fastapi import APIRouter

# ============================================
# CREAR ROUTER PARA HOME
# ============================================
# Un router agrupa endpoints relacionados
router = APIRouter()


# ============================================
# ENDPOINT: GET / (Página de inicio)
# ============================================
# @router.get("/") = Este endpoint responde a peticiones GET en la raíz
# Cuando accedas a: http://localhost:8000/
# Te retornará un mensaje de bienvenida
@router.get("/", summary="Inicio", description="Endpoint principal de la API")
def home():
    """Retorna un mensaje de bienvenida a la API."""
    return {"message": "Clínica Veterinaria"}
