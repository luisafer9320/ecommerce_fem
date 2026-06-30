"""
Modelos SQLAlchemy para Mascotas.
Define la tabla 'mascotas' en la base de datos.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    edad = Column(Integer, nullable=True)
    peso = Column(Float, nullable=True)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    raza_id = Column(Integer, ForeignKey("razas.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    propietario = relationship("Propietario", back_populates="mascotas")
    raza = relationship("Raza", back_populates="mascotas")

    def __repr__(self):
        return f"<Mascota {self.nombre}>"
