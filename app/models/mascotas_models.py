"""
Modelos SQLAlchemy para Mascotas.
Define la tabla 'mascotas' en la base de datos.
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    especie = Column(String(100), nullable=False)
    raza = Column(String(100), nullable=True)
    edad = Column(Integer, nullable=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    propietario = relationship("Propietario", back_populates="mascotas")

    def __repr__(self):
        return f"<Mascota {self.nombre}>"
