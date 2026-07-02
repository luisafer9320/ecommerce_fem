"""
Schemas Pydantic para Mascotas.

Qué es un Schema?
- Define la ESTRUCTURA de los datos que espera recibir o devolver
- Es como un "contrato" que dice:
  "Los datos deben tener estos campos, con estos tipos"
- Valida que los datos sean correctos antes de procesarlos

Qué es Pydantic?
- Una librería que valida datos automáticamente
- Si alguien envía datos incorrectos, Pydantic lo detecta
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

# ============================================
# MascotaBase: Campos comunes de mascota
# ============================================
# Esta es la clase BASE que comparten todos los schemas de mascota
class MascotaBase(BaseModel):
    # Campos que toda mascota DEBE tener
    nombre: str              # Nombre obligatorio
    especie: str             # Especie obligatoria (perro, gato, etc.)
    raza: Optional[str] = None      # Raza opcional
    edad: Optional[int] = None      # Edad opcional
    propietario_id: int      # ID del dueño (obligatorio)

    # ============================================
    # VALIDACIÓN PERSONALIZADA
    # ============================================
    # Esta función se ejecuta automáticamente cuando recibimos datos
    # Valida que nombre y especie no sean campos vacíos
    @field_validator("nombre", "especie")
    @classmethod
    def validar_no_vacio(cls, value: str) -> str:
        # Si el campo está vacío o solo contiene espacios, error
        if not value or not value.strip():
            raise ValueError("El campo no puede estar vacío")
        # Si es válido, retornar sin espacios al inicio/final
        return value.strip()


# ============================================
# MascotaCreate: Schema para CREAR mascota
# ============================================
# Se usa cuando alguien hace POST /mascotas/
# Hereda de MascotaBase (nombre, especie, raza, edad, propietario_id)
class MascotaCreate(MascotaBase):
    """Schema para crear una nueva mascota. Hereda de MascotaBase."""
    pass


# ============================================
# MascotaUpdate: Schema para ACTUALIZAR mascota
# ============================================
# Se usa cuando alguien hace PUT /mascotas/{id}
# TODOS los campos son opcionales (solo actualizar los necesarios)
class MascotaUpdate(BaseModel):
    """Schema para actualizar una mascota. Todos los campos opcionales."""
    nombre: Optional[str] = None              # Opcional
    especie: Optional[str] = None             # Opcional
    raza: Optional[str] = None                # Opcional
    edad: Optional[int] = None                # Opcional
    propietario_id: Optional[int] = None      # Opcional


# ============================================
# MascotaSchema: Schema para DEVOLVER mascota
# ============================================
# Se usa para retornar mascotas desde la API
# Incluye ID y timestamps (created_at, updated_at)
class MascotaSchema(MascotaBase):
    """Schema para retornar una mascota con todos sus datos."""
    id: int                                   # ID único
    is_active: bool = True                    # ¿Está activa?
    created_at: Optional[datetime] = None     # Fecha de creación
    updated_at: Optional[datetime] = None     # Fecha de actualización

    # ============================================
    # CONFIGURACIÓN
    # ============================================
    # from_attributes=True permite convertir objetos SQLAlchemy a Pydantic
    # Sin esto, no podría retornar objetos de la BD
    model_config = {"from_attributes": True}
