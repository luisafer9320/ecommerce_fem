"""
Modelos SQLAlchemy para Razas.
Define la tabla 'razas' en la base de datos.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Raza(Base):
    __tablename__ = "razas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, unique=True, index=True)
    descripcion = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con mascotas
    mascotas = relationship("Mascota", back_populates="raza", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Raza {self.nombre}>"
