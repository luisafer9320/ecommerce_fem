"""
Schemas Pydantic para Propietarios.
"""
from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from datetime import datetime

class PropietarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    is_active: Optional[bool] = True

    @validator('nombre', 'apellido')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip()

class PropietarioCreate(PropietarioBase):
    """Schema para crear un propietario."""
    pass

class PropietarioUpdate(BaseModel):
    """Schema para actualizar un propietario."""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    is_active: Optional[bool] = None

class PropietarioSchema(PropietarioBase):
    """Schema para retornar un propietario."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
