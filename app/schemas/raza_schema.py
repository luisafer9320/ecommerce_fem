"""
Schemas Pydantic para Razas.
Define los DTOs (Data Transfer Objects) para entrada/salida de la API.
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class RazaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

class RazaCreate(RazaBase):
    """Schema para crear una raza."""
    pass

class RazaUpdate(BaseModel):
    """Schema para actualizar una raza."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class RazaSchema(RazaBase):
    """Schema para retornar una raza."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
