# 📊 Esquema de Base de Datos - Clínica Veterinaria

## Base de Datos: SQLite
**Archivo:** `clinica_veterinaria.db`

---

## 📋 Tablas

### 1. **RAZAS**
Almacena las razas de mascotas disponibles.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PRIMARY KEY | Identificador único |
| nombre | VARCHAR(200) | NOT NULL, UNIQUE | Nombre de la raza |
| descripcion | TEXT | NULL | Descripción opcional |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NULL | Fecha de última actualización |

**Índices:**
- `ix_razas_id` - Índice en id
- `ix_razas_nombre` - Índice único en nombre

---

### 2. **PROPIETARIOS**
Almacena la información de los propietarios de mascotas.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PRIMARY KEY | Identificador único |
| nombre | VARCHAR(200) | NOT NULL | Nombre del propietario |
| apellido | VARCHAR(200) | NOT NULL | Apellido del propietario |
| email | VARCHAR(200) | NOT NULL, UNIQUE | Email del propietario |
| telefono | VARCHAR(20) | NULL | Teléfono de contacto |
| direccion | TEXT | NULL | Dirección del propietario |
| is_active | BOOLEAN | DEFAULT TRUE | Estado del propietario |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NULL | Fecha de última actualización |

**Índices:**
- `ix_propietarios_id` - Índice en id
- `ix_propietarios_email` - Índice único en email
- `ix_propietarios_nombre` - Índice en nombre

---

### 3. **MASCOTAS**
Almacena la información de las mascotas registradas.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PRIMARY KEY | Identificador único |
| nombre | VARCHAR(200) | NOT NULL | Nombre de la mascota |
| edad | INTEGER | NULL | Edad de la mascota |
| peso | FLOAT | NULL | Peso en kg |
| propietario_id | INTEGER | FK → propietarios(id) | Referencia al propietario |
| raza_id | INTEGER | FK → razas(id) | Referencia a la raza |
| is_active | BOOLEAN | DEFAULT TRUE | Estado de la mascota |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | NULL | Fecha de última actualización |

**Índices:**
- `ix_mascotas_id` - Índice en id
- `ix_mascotas_nombre` - Índice en nombre

**Foreign Keys:**
- `propietario_id` → `propietarios(id)`
- `raza_id` → `razas(id)`

---

## 🔗 Relaciones

```
PROPIETARIOS (1) ────── (N) MASCOTAS
                           │
                           │ (N)
                           │
                           ├─→ (1) RAZAS
```

- Un **Propietario** puede tener múltiples **Mascotas**
- Una **Mascota** pertenece a un **Propietario** y tiene una **Raza**
- Una **Raza** puede tener múltiples **Mascotas**

---

## 📌 Configuración Actual

### Base de Datos
- **Tipo:** SQLite (desarrollo local)
- **URL:** `sqlite:///./clinica_veterinaria.db`
- **Ubicación:** Raíz del proyecto

### Para Producción (PostgreSQL)
Cambiar en `.env`:
```
DATABASE_URL=postgresql://usuario:password@localhost:5432/clinica_veterinaria
```

---

## 🐘 Conexión con pgAdmin (PostgreSQL)

### Requisitos:
1. **PostgreSQL** instalado y corriendo
2. **pgAdmin** instalado (http://localhost:5050)

### Pasos para conectar:
1. Abre pgAdmin en tu navegador
2. Haz clic en "Agregar nuevo servidor"
3. Configura:
   - **Nombre:** clinica_veterinaria
   - **Host:** localhost
   - **Puerto:** 5432
   - **Usuario:** postgres (o tu usuario)
   - **Contraseña:** (tu contraseña)
4. Crea la base de datos: `clinica_veterinaria`
5. Actualiza `.env`:
   ```
   DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/clinica_veterinaria
   ```
6. Reinicia el servidor FastAPI

---

## ✅ Estado Actual del Proyecto

- ✅ Base de datos SQLite funcional
- ✅ 3 tablas creadas (razas, propietarios, mascotas)
- ✅ Relaciones configuradas
- ✅ Índices optimizados
- ✅ Servidor FastAPI activo en http://127.0.0.1:8000
- ✅ Documentación Swagger en http://127.0.0.1:8000/docs

---

## 📚 Endpoints Disponibles

### Razas
- `POST /razas/` - Crear raza
- `GET /razas/` - Listar razas
- `GET /razas/{id}` - Obtener raza
- `PUT /razas/{id}` - Actualizar raza
- `DELETE /razas/{id}` - Eliminar raza

### Propietarios
- `POST /propietarios/` - Crear propietario
- `GET /propietarios/` - Listar propietarios
- `GET /propietarios/{id}` - Obtener propietario
- `PUT /propietarios/{id}` - Actualizar propietario
- `DELETE /propietarios/{id}` - Eliminar propietario

### Mascotas
- `POST /mascotas/` - Crear mascota
- `GET /mascotas/` - Listar mascotas
- `GET /mascotas/{id}` - Obtener mascota
- `PUT /mascotas/{id}` - Actualizar mascota
- `DELETE /mascotas/{id}` - Eliminar mascota

---

**Última actualización:** 2026-06-30
