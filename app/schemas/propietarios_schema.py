"""
Schemas Pydantic para Propietarios.

Este archivo define qué datos espera recibir y devolver para Propietarios.
Pydantic valida automáticamente que los datos sean correctos.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


# ============================================
# PropietarioBase: Campos comunes del propietario
# ============================================
class PropietarioBase(BaseModel):
    """Base con los campos principales de un propietario."""
    # Campos obligatorios
    nombre: str              # Nombre obligatorio
    apellido: str            # Apellido obligatorio
    email: EmailStr          # Email obligatorio (EmailStr valida formato)
    
    # Campos opcionales
    telefono: Optional[str] = None           # Teléfono opcional
    direccion: Optional[str] = None          # Dirección opcional
    is_active: Optional[bool] = True         # Activo por defecto

    # ============================================
    # VALIDACIÓN PERSONALIZADA
    # ============================================
    # Valida que nombre y apellido no sean vacíos
    @field_validator('nombre', 'apellido')
    @classmethod
    def nombre_no_vacio(cls, v):
        """Valida que nombre y apellido no estén vacíos."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip()

# ============================================
# PropietarioCreate: Schema para CREAR propietario
# ============================================
class PropietarioCreate(PropietarioBase):
    """Schema para crear un nuevo propietario.
    
    Se usa en: POST /propietarios/
    Hereda todos los campos de PropietarioBase.
    """
    pass


# ============================================
# PropietarioUpdate: Schema para ACTUALIZAR propietario
# ============================================
class PropietarioUpdate(BaseModel):
    """Schema para actualizar un propietario.
    
    Se usa en: PUT /propietarios/{id}
    TODOS los campos son opcionales.
    Solo se actualizan los campos enviados.
    """
    nombre: Optional[str] = None             # Opcional
    apellido: Optional[str] = None           # Opcional
    email: Optional[EmailStr] = None         # Opcional
    telefono: Optional[str] = None           # Opcional
    direccion: Optional[str] = None          # Opcional
    is_active: Optional[bool] = None         # Opcional


# ============================================
# PropietarioSchema: Schema para DEVOLVER propietario
# ============================================
class PropietarioSchema(PropietarioBase):
    """Schema para retornar un propietario desde la API.
    
    Se usa para devolver propietarios en respuestas.
    Incluye ID y timestamps.
    """
    id: int                                  # ID único
    created_at: Optional[datetime] = None    # Fecha de creación
    updated_at: Optional[datetime] = None    # Fecha de última actualización

    # ============================================
    # CONFIGURACIÓN
    # ============================================
    # from_attributes=True: Permite convertir objetos SQLAlchemy a Pydantic
    model_config = {"from_attributes": True}
