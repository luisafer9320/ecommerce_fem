"""
Schemas Pydantic para Propietarios.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class PropietarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    is_active: Optional[bool] = True

    @field_validator('nombre', 'apellido')
    @classmethod
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

    model_config = {"from_attributes": True}
