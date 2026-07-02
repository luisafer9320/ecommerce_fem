"""
Router para endpoints de Propietarios.
CRUD completo: Create, Read, Update, Delete

Qué es CRUD?
  C = Create (Crear) → POST
  R = Read (Leer) → GET
  U = Update (Actualizar) → PUT
  D = Delete (Eliminar) → DELETE

Este archivo define todas las operaciones que puedes hacer con propietarios.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.propietarios_models import Propietario
from app.schemas.propietarios_schema import PropietarioSchema, PropietarioCreate, PropietarioUpdate

# ============================================
# CREAR ROUTER PARA PROPIETARIOS
# ============================================
# prefix="/propietarios" = todos los endpoints empiezan con /propietarios
# tags=["Propietarios"] = agrupa estos endpoints en la documentación
router = APIRouter(prefix="/propietarios", tags=["Propietarios"])

# ============================================
# CREAR PROPIETARIO - POST /propietarios/
# ============================================
# @router.post("/") = responde a peticiones POST
# response_model = devuelve los datos en formato PropietarioSchema
# status_code = código HTTP 201 (Creado exitosamente)
@router.post("/", response_model=PropietarioSchema, status_code=status.HTTP_201_CREATED, summary="Crear Propietario")
def crear_propietario(propietario: PropietarioCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo propietario.
    
    Pasos que hace esta función:
    1. Verifica que el email no esté registrado (emails únicos)
    2. Si el email ya existe, lanza error
    3. Si no existe, crea un nuevo propietario
    4. Guarda en la BD con db.commit()
    5. Retorna los datos del nuevo propietario
    """
    # Buscar si el email ya existe en la BD
    db_email = db.query(Propietario).filter(Propietario.email == propietario.email).first()
    if db_email:
        # Si existe, lanzar error 400 (Solicitud inválida)
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear nueva instancia de Propietario con los datos recibidos
    nuevo_propietario = Propietario(**propietario.dict())
    
    # Agregar a la sesión de BD
    db.add(nuevo_propietario)
    
    # Guardar los cambios en la BD
    db.commit()
    
    # Actualizar el objeto con datos de BD (como el ID generado)
    db.refresh(nuevo_propietario)
    
    # Retornar el propietario creado
    return nuevo_propietario

# ============================================
# LISTAR PROPIETARIOS - GET /propietarios/
# ============================================
# @router.get("/") = responde a peticiones GET
# response_model=List[...] = retorna una LISTA de propietarios
# skip y limit = para PAGINAR resultados
@router.get("/", response_model=List[PropietarioSchema], summary="Listar Propietarios")
def listar_propietarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de todos los propietarios.
    
    Parámetros:
    - skip: Cuántos registros saltar (para paginar)
    - limit: Cuántos registros traer máximo (por defecto 100)
    
    Ejemplo: /propietarios/?skip=0&limit=10
             Trae los primeros 10 propietarios
    """
    # Consultar todos los propietarios con paginación
    propietarios = db.query(Propietario).offset(skip).limit(limit).all()
    return propietarios

# ============================================
# OBTENER UN PROPIETARIO - GET /propietarios/{id}
# ============================================
# {propietario_id} = parámetro dinámico en la URL
# Ejemplo: GET /propietarios/1 (obtiene propietario con ID 1)
@router.get("/{propietario_id}", response_model=PropietarioSchema, summary="Obtener Propietario")
def obtener_propietario(propietario_id: int, db: Session = Depends(get_db)):
    """
    Obtener un propietario específico por su ID.
    
    Pasos:
    1. Buscar el propietario en la BD
    2. Si no existe, retornar error 404
    3. Si existe, retornarlo
    """
    # Buscar propietario con ID específico
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    
    # Si no existe, lanzar error 404 (No encontrado)
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    
    return propietario

# ============================================
# ACTUALIZAR PROPIETARIO - PUT /propietarios/{id}
# ============================================
# PUT = actualizar datos existentes
# exclude_unset=True = solo actualizar campos que fueron enviados
@router.put("/{propietario_id}", response_model=PropietarioSchema, summary="Actualizar Propietario")
def actualizar_propietario(propietario_id: int, propietario_update: PropietarioUpdate, db: Session = Depends(get_db)):
    """
    Actualizar los datos de un propietario.
    
    Pasos:
    1. Buscar el propietario
    2. Si no existe, retornar error 404
    3. Actualizar solo los campos enviados
    4. Guardar cambios en la BD
    5. Retornar propietario actualizado
    """
    # Buscar el propietario a actualizar
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    
    # Actualizar solo los campos que fueron enviados
    # exclude_unset=True = no actualizar campos no enviados
    for key, value in propietario_update.dict(exclude_unset=True).items():
        # setattr() = asignar valor a un atributo de forma dinámica
        setattr(propietario, key, value)
    
    # Guardar cambios
    db.commit()
    
    # Actualizar objeto local con datos de BD
    db.refresh(propietario)
    
    return propietario

# ============================================
# ELIMINAR PROPIETARIO - DELETE /propietarios/{id}
# ============================================
# DELETE = eliminar datos
# status_code=204 = No Content (eliminado exitosamente, sin contenido)
@router.delete("/{propietario_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Propietario")
def eliminar_propietario(propietario_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un propietario y todas sus mascotas (cascade delete).
    
    Pasos:
    1. Buscar el propietario
    2. Si no existe, retornar error 404
    3. Eliminarlo de la BD
    4. Sus mascotas también se eliminan automáticamente (cascade)
    5. Retornar 204 (sin contenido)
    """
    # Buscar el propietario
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if not propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    
    # Eliminar de la BD
    db.delete(propietario)
    
    # Guardar cambios
    db.commit()
    
    # Retornar None (204 no tiene contenido)
    return None

