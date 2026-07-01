from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Inicio", description="Endpoint principal de la API")
def home():
    return {"message": "Clínica Veterinaria"}
