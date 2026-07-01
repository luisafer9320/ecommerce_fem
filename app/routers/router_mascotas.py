"""
Router para endpoints de Mascotas.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.mascotas_models import Mascota
from app.models.propietarios_models import Propietario
from app.schemas.mascotas_schema import MascotaCreate, MascotaSchema, MascotaUpdate

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])


@router.post("/", response_model=MascotaSchema, status_code=status.HTTP_201_CREATED, summary="Crear Mascota")
def crear_mascota(mascota: MascotaCreate, db: Session = Depends(get_db)):
    propietario = db.query(Propietario).filter(Propietario.id == mascota.propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

    nueva_mascota = Mascota(**mascota.model_dump())
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota


@router.get("/", response_model=List[MascotaSchema], summary="Listar Mascotas")
def listar_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Mascota).offset(skip).limit(limit).all()


@router.get("/{mascota_id}", response_model=MascotaSchema, summary="Obtener Mascota")
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota


@router.put("/{mascota_id}", response_model=MascotaSchema, summary="Actualizar Mascota")
def actualizar_mascota(mascota_id: int, mascota_update: MascotaUpdate, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    for key, value in mascota_update.model_dump(exclude_unset=True).items():
        setattr(mascota, key, value)

    db.commit()
    db.refresh(mascota)
    return mascota


@router.delete("/{mascota_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Mascota")
def eliminar_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    db.delete(mascota)
    db.commit()
    return None
