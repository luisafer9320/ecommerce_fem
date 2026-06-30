"""
Router para endpoints de Mascotas.
CRUD completo: Create, Read, Update, Delete
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.mascotas_models import Mascota
from app.schemas.mascotas_schema import MascotaSchema, MascotaCreate, MascotaUpdate

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

@router.post("/", response_model=MascotaSchema, status_code=status.HTTP_201_CREATED, summary="Crear Mascota")
def crear_mascota(mascota: MascotaCreate, db: Session = Depends(get_db)):
    """Crear una nueva mascota"""
    nueva_mascota = Mascota(**mascota.dict())
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

@router.get("/", response_model=List[MascotaSchema], summary="Listar Mascotas")
def listar_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las mascotas"""
    mascotas = db.query(Mascota).offset(skip).limit(limit).all()
    return mascotas

@router.get("/{mascota_id}", response_model=MascotaSchema, summary="Obtener Mascota")
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """Obtener una mascota por ID"""
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

@router.put("/{mascota_id}", response_model=MascotaSchema, summary="Actualizar Mascota")
def actualizar_mascota(mascota_id: int, mascota_update: MascotaUpdate, db: Session = Depends(get_db)):
    """Actualizar los datos de una mascota"""
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    for key, value in mascota_update.dict(exclude_unset=True).items():
        setattr(mascota, key, value)
    
    db.commit()
    db.refresh(mascota)
    return mascota

@router.delete("/{mascota_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Mascota")
def eliminar_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """Eliminar una mascota"""
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    db.delete(mascota)
    db.commit()
    return None

