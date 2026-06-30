"""
Router para endpoints de Propietarios.
CRUD completo: Create, Read, Update, Delete
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.propietarios_models import Propietario
from app.schemas.propietarios_schema import PropietarioSchema, PropietarioCreate, PropietarioUpdate

router = APIRouter(prefix="/propietarios", tags=["Propietarios"])

@router.post("/", response_model=PropietarioSchema, status_code=status.HTTP_201_CREATED, summary="Crear Propietario")
def crear_propietario(propietario: PropietarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo propietario"""
    db_email = db.query(Propietario).filter(Propietario.email == propietario.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_propietario = Propietario(**propietario.dict())
    db.add(nuevo_propietario)
    db.commit()
    db.refresh(nuevo_propietario)
    return nuevo_propietario

@router.get("/", response_model=List[PropietarioSchema], summary="Listar Propietarios")
def listar_propietarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todos los propietarios"""
    propietarios = db.query(Propietario).offset(skip).limit(limit).all()
    return propietarios

@router.get("/{propietario_id}", response_model=PropietarioSchema, summary="Obtener Propietario")
def obtener_propietario(propietario_id: int, db: Session = Depends(get_db)):
    """Obtener un propietario por ID"""
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return propietario

@router.put("/{propietario_id}", response_model=PropietarioSchema, summary="Actualizar Propietario")
def actualizar_propietario(propietario_id: int, propietario_update: PropietarioUpdate, db: Session = Depends(get_db)):
    """Actualizar los datos de un propietario"""
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    
    for key, value in propietario_update.dict(exclude_unset=True).items():
        setattr(propietario, key, value)
    
    db.commit()
    db.refresh(propietario)
    return propietario

@router.delete("/{propietario_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Propietario")
def eliminar_propietario(propietario_id: int, db: Session = Depends(get_db)):
    """Eliminar un propietario"""
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    
    db.delete(propietario)
    db.commit()
    return None

