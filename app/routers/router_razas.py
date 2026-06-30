"""
Router para endpoints de Razas.
CRUD completo: Create, Read, Update, Delete
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.razas_models import Raza
from app.schemas.raza_schema import RazaSchema, RazaCreate, RazaUpdate

router = APIRouter(prefix="/razas", tags=["Razas"])

@router.post("/", response_model=RazaSchema, status_code=status.HTTP_201_CREATED, summary="Crear Raza")
def crear_raza(raza: RazaCreate, db: Session = Depends(get_db)):
    """Crear una nueva raza de mascota"""
    db_raza = db.query(Raza).filter(Raza.nombre == raza.nombre).first()
    if db_raza:
        raise HTTPException(status_code=400, detail="La raza ya existe")
    
    nueva_raza = Raza(**raza.dict())
    db.add(nueva_raza)
    db.commit()
    db.refresh(nueva_raza)
    return nueva_raza

@router.get("/", response_model=List[RazaSchema], summary="Listar Razas")
def listar_razas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las razas"""
    razas = db.query(Raza).offset(skip).limit(limit).all()
    return razas

@router.get("/{raza_id}", response_model=RazaSchema, summary="Obtener Raza")
def obtener_raza(raza_id: int, db: Session = Depends(get_db)):
    """Obtener una raza por ID"""
    raza = db.query(Raza).filter(Raza.id == raza_id).first()
    if not raza:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    return raza

@router.put("/{raza_id}", response_model=RazaSchema, summary="Actualizar Raza")
def actualizar_raza(raza_id: int, raza_update: RazaUpdate, db: Session = Depends(get_db)):
    """Actualizar los datos de una raza"""
    raza = db.query(Raza).filter(Raza.id == raza_id).first()
    if not raza:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    
    for key, value in raza_update.dict(exclude_unset=True).items():
        setattr(raza, key, value)
    
    db.commit()
    db.refresh(raza)
    return raza

@router.delete("/{raza_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Raza")
def eliminar_raza(raza_id: int, db: Session = Depends(get_db)):
    """Eliminar una raza"""
    raza = db.query(Raza).filter(Raza.id == raza_id).first()
    if not raza:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    
    db.delete(raza)
    db.commit()
    return None

