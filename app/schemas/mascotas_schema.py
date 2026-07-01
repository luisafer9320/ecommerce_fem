"""
Schemas Pydantic para Mascotas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    propietario_id: int

    @field_validator("nombre", "especie")
    @classmethod
    def validar_no_vacio(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("El campo no puede estar vacío")
        return value.strip()


class MascotaCreate(MascotaBase):
    pass


class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = None
    propietario_id: Optional[int] = None


class MascotaSchema(MascotaBase):
    id: int
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
