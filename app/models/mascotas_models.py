"""
Modelos SQLAlchemy para Mascotas.
Define la tabla 'mascotas' en la base de datos.

Un modelo es como un MOLDE que define:
- Qué datos vamos a guardar (nombre, especie, etc.)
- Cómo se guardan en la BD (tipo de dato, si es obligatorio, etc.)
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class Mascota(Base):
    # ============================================
    # TABLA 'mascotas' EN LA BASE DE DATOS
    # ============================================
    __tablename__ = "mascotas"

    # ============================================
    # CAMPOS DE LA MASCOTA
    # ============================================
    # id: Identificador único de cada mascota (clave primaria)
    #     index=True hace que las búsquedas por ID sean más rápidas
    id = Column(Integer, primary_key=True, index=True)
    
    # nombre: El nombre de la mascota
    #         String(200) = texto de máximo 200 caracteres
    #         nullable=False = OBLIGATORIO
    #         index=True = búsquedas por nombre serán más rápidas
    nombre = Column(String(200), nullable=False, index=True)
    
    # especie: Tipo de animal (gato, perro, pajaro, etc.)
    #          nullable=False = OBLIGATORIO
    especie = Column(String(100), nullable=False)
    
    # raza: Raza específica (Bulldog, Siamés, etc.)
    #       nullable=True = OPCIONAL (puede ser NULL)
    raza = Column(String(100), nullable=True)
    
    # edad: Edad en años
    #       Integer = número entero
    #       nullable=True = OPCIONAL
    edad = Column(Integer, nullable=True)
    
    # propietario_id: ID del propietario de la mascota
    #                 ForeignKey vincula con la tabla propietarios
    #                 Esto significa: "Esta mascota PERTENECE a un propietario"
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    
    # is_active: ¿Está activa la mascota?
    #            Boolean = verdadero/falso
    #            default=True = por defecto está activa
    is_active = Column(Boolean, default=True)
    
    # created_at: Fecha y hora cuando se creó el registro
    #             server_default=func.now() = se calcula automáticamente en la BD
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # updated_at: Fecha y hora de la última actualización
    #             onupdate=func.now() = se actualiza automáticamente cada vez que se modifica
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ============================================
    # RELACIÓN CON PROPIETARIO
    # ============================================
    # Esto permite acceder fácilmente a los datos del propietario
    # Ejemplo: mascota.propietario.nombre (obtiene el nombre del propietario)
    propietario = relationship("Propietario", back_populates="mascotas")

    # ============================================
    # REPRESENTACIÓN EN TEXTO
    # ============================================
    # Esto hace que cuando imprimas la mascota, vea algo bonito
    def __repr__(self):
        return f"<Mascota {self.nombre}>"
