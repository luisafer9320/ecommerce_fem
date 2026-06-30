"""
Schemas Pydantic para Mascotas.
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class MascotaBase(BaseModel):
    nombre: str
    edad: Optional[int] = None
    peso: Optional[float] = None
    propietario_id: int
    raza_id: int
    is_active: Optional[bool] = True

    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @validator('edad')
    def edad_valida(cls, v):
        if v is not None and v < 0:
            raise ValueError('La edad no puede ser negativa')
        return v

    @validator('peso')
    def peso_valido(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El peso debe ser mayor que 0')
        return v

class MascotaCreate(MascotaBase):
    """Schema para crear una mascota."""
    pass

class MascotaUpdate(BaseModel):
    """Schema para actualizar una mascota."""
    nombre: Optional[str] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    propietario_id: Optional[int] = None
    raza_id: Optional[int] = None
    is_active: Optional[bool] = None

class MascotaSchema(MascotaBase):
    """Schema para retornar una mascota."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
