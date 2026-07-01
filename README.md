# Clínica Veterinaria API - FastAPI

API REST para gestionar una clínica veterinaria construida con **FastAPI**, **SQLAlchemy** y **SQLite** (desarrollo) / **PostgreSQL** (producción).

## ✅ Estado Actual - LISTO PARA TALLER

- ✅ Estructura limpia y organizada
- ✅ CRUD completo: Razas, Propietarios, Mascotas
- ✅ Base de datos funcional (SQLite por defecto)
- ✅ Validaciones con Pydantic
- ✅ Documentación OpenAPI (Swagger)
- ✅ Servidor running en http://127.0.0.1:8000
- ✅ Listo para cambiar a PostgreSQL/pgAdmin

## 🎯 Características

- ✅ CRUD completo: Razas, Propietarios, Mascotas
- ✅ Base de datos SQLite (desarrollo) / PostgreSQL (producción)
- ✅ Validaciones con Pydantic
- ✅ Documentación OpenAPI automática (Swagger)
- ✅ Estructura profesional y escalable
- ✅ Relaciones entre entidades (One-to-Many)

## 📁 Estructura del Proyecto

```
ecommerce_fem/
├── app/
│   ├── __init__.py
│   ├── db.py                     # Conexión a BD + Base class
│   ├── models/                   # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── razas_models.py       # Modelo Raza
│   │   ├── propietarios_models.py # Modelo Propietario
│   │   └── mascotas_models.py    # Modelo Mascota
│   ├── schemas/                  # Schemas Pydantic (validación)
│   │   ├── __init__.py
│   │   ├── raza_schema.py        # DTOs para Razas
│   │   ├── propietarios_schema.py # DTOs para Propietarios
│   │   └── mascotas_schema.py    # DTOs para Mascotas
│   └── routers/                  # Endpoints FastAPI
│       ├── __init__.py
│       ├── router_home.py        # Endpoint raíz
│       ├── router_razas.py       # CRUD Razas
│       ├── router_propietarios.py # CRUD Propietarios
│       └── router_mascotas.py    # CRUD Mascotas
├── main.py                       # Punto de entrada
├── .env                          # Variables de entorno
├── requirements.txt              # Dependencias
├── SCHEMA_BD.md                  # Esquema completo de BD
└── README.md                     # Este archivo
```

## 🚀 Instalación Rápida



### 1. Activar entorno virtual
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar servidor
```bash
python -m uvicorn main:app --reload
```

**El servidor estará en:** http://127.0.0.1:8000

## 📚 Documentación

- **Swagger UI (Recomendado)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Schema BD**: Ver archivo `SCHEMA_BD.md`

## 💾 Base de Datos

### Configuración Actual: SQLite
```
DATABASE_URL=sqlite:///./clinica_veterinaria.db
```
✅ No requiere instalación extra
✅ Perfecta para desarrollo local

### Cambiar a PostgreSQL (Producción)

#### Paso 1: Verificar PostgreSQL
```bash
# Windows - verificar si PostgreSQL está corriendo
Get-Service postgres  # Si existe

# macOS
brew services list | grep postgres
```

#### Paso 2: Crear base de datos
```bash
psql -U postgres -c "CREATE DATABASE clinica_veterinaria;"
```

#### Paso 3: Actualizar .env
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/clinica_veterinaria
```

#### Paso 4: Instalar driver
```bash
pip install psycopg2-binary
```

#### Paso 5: Reiniciar servidor
```bash
python -m uvicorn main:app --reload
```

## 🔒 Mejoras Futuras

- [ ] Autenticación (JWT)
- [ ] Autorización (roles)
- [ ] Historial de citas
- [ ] Expediente clínico de mascotas
- [ ] Notificaciones por email
- [ ] Caché con Redis
- [ ] Rate limiting
- [ ] Documentación API con Postman
- [ ] Containerización con Docker

## 📚 Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| FastAPI | 0.138.0 | Framework web async |
| SQLAlchemy | 2.0.51 | ORM async |
| asyncpg | 0.31.0 | Driver PostgreSQL async |
| Pydantic | 2.13.4 | Validación de datos |
| Alembic | 1.18.5 | Migraciones BD |
| pytest | 9.1.1 | Testing |
| uvicorn | 0.49.0 | Servidor ASGI |

## 🤝 Contribuciones

Este proyecto es un ejemplo de aprendizaje en el **Bootcamp FemCoders Madrid P5**.

## 📄 Licencia

MIT

---