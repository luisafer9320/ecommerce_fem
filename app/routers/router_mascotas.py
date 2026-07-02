"""
Router para endpoints de Mascotas.

Este archivo gestiona todas las operaciones con mascotas:
- Crear mascotas
- Listar mascotas
- Obtener una mascota específica
- Actualizar datos de una mascota
- Eliminar una mascota
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.mascotas_models import Mascota
from app.models.propietarios_models import Propietario
from app.schemas.mascotas_schema import MascotaCreate, MascotaSchema, MascotaUpdate

# ============================================
# CREAR ROUTER PARA MASCOTAS
# ============================================
router = APIRouter(prefix="/mascotas", tags=["Mascotas"])


# ============================================
# CREAR MASCOTA - POST /mascotas/
# ============================================
@router.post("/", response_model=MascotaSchema, status_code=status.HTTP_201_CREATED, summary="Crear Mascota")
def crear_mascota(mascota: MascotaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva mascota.
    
    Validación importante:
    - El propietario_id debe existir en la BD
    - Si no existe, retorna error 404
    
    Pasos:
    1. Verificar que el propietario existe
    2. Crear nueva mascota
    3. Guardar en BD
    4. Retornar mascota creada
    """
    # Buscar el propietario para verificar que existe
    propietario = db.query(Propietario).filter(Propietario.id == mascota.propietario_id).first()
    if not propietario:
        # Si no existe el propietario, error 404
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    # Crear nueva instancia de Mascota
    nueva_mascota = Mascota(**mascota.model_dump())
    
    # Agregar a sesión
    db.add(nueva_mascota)
    
    # Guardar
    db.commit()
    
    # Actualizar con datos de BD
    db.refresh(nueva_mascota)
    
    return nueva_mascota


# ============================================
# LISTAR MASCOTAS - GET /mascotas/
# ============================================
# Con paginación para no traer demasiados datos a la vez
@router.get("/", response_model=List[MascotaSchema], summary="Listar Mascotas")
def listar_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de todas las mascotas.
    
    Parámetros de paginación:
    - skip: Cuántos registros saltar (para ir a la siguiente página)
    - limit: Cuántos registros traer máximo
    
    Ejemplo: /mascotas/?skip=0&limit=10
             Trae mascotas 1-10
    """
    return db.query(Mascota).offset(skip).limit(limit).all()


# ============================================
# OBTENER UNA MASCOTA - GET /mascotas/{id}
# ============================================
@router.get("/{mascota_id}", response_model=MascotaSchema, summary="Obtener Mascota")
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """
    Obtener una mascota específica por su ID.
    
    Ejemplo: GET /mascotas/5
             Retorna la mascota con ID 5
    """
    # Buscar mascota por ID
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    
    # Si no existe, error 404
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    return mascota


# ============================================
# ACTUALIZAR MASCOTA - PUT /mascotas/{id}
# ============================================
@router.put("/{mascota_id}", response_model=MascotaSchema, summary="Actualizar Mascota")
def actualizar_mascota(mascota_id: int, mascota_update: MascotaUpdate, db: Session = Depends(get_db)):
    """
    Actualizar los datos de una mascota.
    
    Solo se actualizan los campos que se envían.
    Campos no enviados permanecen sin cambios.
    """
    # Buscar mascota
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Actualizar solo campos enviados
    for key, value in mascota_update.model_dump(exclude_unset=True).items():
        setattr(mascota, key, value)

    # Guardar cambios
    db.commit()
    db.refresh(mascota)
    
    return mascota


# ============================================
# ELIMINAR MASCOTA - DELETE /mascotas/{id}
# ============================================
@router.delete("/{mascota_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Mascota")
def eliminar_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una mascota de la BD.
    
    Nota: El propietario NO se elimina, solo la mascota.
    """
    # Buscar mascota
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Eliminar de BD
    db.delete(mascota)
    db.commit()
    
    return None
