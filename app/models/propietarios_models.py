"""
Modelos SQLAlchemy para Propietarios.
Define la tabla 'propietarios' en la base de datos.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Propietario(Base):
    __tablename__ = "propietarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    apellido = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con mascotas
    mascotas = relationship("Mascota", back_populates="propietario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Propietario {self.nombre} {self.apellido}>"
