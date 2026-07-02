"""
Modelos SQLAlchemy para Propietarios.
Define la tabla 'propietarios' en la base de datos.

Un Propietario es una PERSONA que dueña de una o más mascotas.
Este modelo guarda todos sus datos.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Propietario(Base):
    # ============================================
    # TABLA 'propietarios' EN LA BASE DE DATOS
    # ============================================
    __tablename__ = "propietarios"

    # ============================================
    # CAMPOS DEL PROPIETARIO
    # ============================================
    # id: Identificador único de cada propietario
    id = Column(Integer, primary_key=True, index=True)
    
    # nombre: Nombre del propietario (Juan, María, etc.)
    #         nullable=False = OBLIGATORIO
    nombre = Column(String(200), nullable=False, index=True)
    
    # apellido: Apellido del propietario
    #           nullable=False = OBLIGATORIO
    apellido = Column(String(200), nullable=False)
    
    # email: Correo electrónico del propietario
    #        unique=True = NO puede haber dos propietarios con el mismo email
    #        nullable=False = OBLIGATORIO
    email = Column(String(200), unique=True, index=True, nullable=False)
    
    # telefono: Número de teléfono
    #           nullable=True = OPCIONAL
    telefono = Column(String(20), nullable=True)
    
    # direccion: Dirección de la casa
    #            Text = texto más largo (no limitado a 200 caracteres)
    #            nullable=True = OPCIONAL
    direccion = Column(Text, nullable=True)
    
    # is_active: ¿Está activo el propietario?
    #            default=True = por defecto está activo
    is_active = Column(Boolean, default=True)
    
    # created_at: Fecha de registro
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # updated_at: Fecha de última actualización
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ============================================
    # RELACIÓN CON MASCOTAS
    # ============================================
    # cascade="all, delete-orphan" significa:
    #   Si eliminas un propietario, también se eliminan TODAS sus mascotas
    #   Esto evita dejar mascotas sin dueño
    mascotas = relationship("Mascota", back_populates="propietario", cascade="all, delete-orphan")

    # ============================================
    # REPRESENTACIÓN EN TEXTO
    # ============================================
    def __repr__(self):
        return f"<Propietario {self.nombre} {self.apellido}>"
