"""
ARCHIVO DE TESTS PARA LA API DE CLÍNICA VETERINARIA.

¿QUÉ SON TESTS?
- Pruebas automáticas que verifican que tu código funciona correctamente
- Son como un ROBOT que prueba tu API sin que tengas que hacerlo manualmente
- Si algo se rompe, los tests lo detectan inmediatamente

¿CÓMO EJECUTAR?
    pytest test_main.py        # Ejecutar todos los tests
    pytest test_main.py -v     # Con más detalles (verbose)
"""

# ============================================
# IMPORTACIONES
# ============================================
from uuid import uuid4
# uuid4(): Genera códigos únicos (ejemplo: a1b2c3d4e5f6)
# Los usamos para crear emails únicos en los tests

from fastapi.testclient import TestClient
# TestClient: Cliente que simula un usuario haciendo peticiones HTTP
# SIN necesidad de levantar un servidor real

from main import app
# Importar la aplicación FastAPI que queremos probar


# ============================================
# CREAR CLIENTE DE PRUEBA
# ============================================
# Este cliente puede simular peticiones HTTP a nuestra API
# Nos permite hacer: client.get(), client.post(), client.put(), client.delete()
client = TestClient(app)

# ============================================
# TEST 1: Verificar que la documentación existe
# ============================================
def test_docs_available():
    """
    Verifica que la documentación de la API está disponible en /docs.
    
    ¿Por qué?
    - La documentación es importante para que otros entiendan cómo usar la API
    - Si este test falla, significa que algo fundamental está roto
    """
    # Hacer una petición GET a /docs (documentación Swagger)
    response = client.get("/docs")
    
    # assert = afirmación = "esto DEBE ser verdadero"
    # Si no es verdadero, el test falla
    # status_code 200 = éxito (la página existe)
    assert response.status_code == 200
    # ✅ Si retorna 200: TEST PASA
    # ❌ Si retorna 404 o cualquier otro código: TEST FALLA


# ============================================
# TEST 2: Crear propietario Y mascota (caso exitoso)
# ============================================
def test_crear_propietario_y_mascota():
    """
    Este es el TEST MÁS IMPORTANTE.
    Verifica que podemos:
    1. Crear un propietario
    2. Crear una mascota vinculada a ese propietario
    
    Esto prueba el flujo COMPLETO de la aplicación.
    """
    
    # ============================================
    # PASO 1: Generar email único
    # ============================================
    # uuid4().hex genera un código único como: a1b2c3d4e5f6
    # Lo usamos para que cada test tenga un email diferente
    # Sin esto, el test fallaría la 2ª ejecución (email duplicado)
    email = f"usuario-{uuid4().hex}@mail.com"
    # Resultado: "usuario-a1b2c3d4e5f6@mail.com"

    # ============================================
    # PASO 2: Preparar datos del PROPIETARIO
    # ============================================
    # Este es el JSON que vamos a enviar en la petición POST
    propietario_payload = {
        "nombre": "Ana",
        "apellido": "Pérez",
        "email": email,                # Email único generado arriba
        "telefono": "600123456",
        "direccion": "Calle Mayor 1",
    }

    # ============================================
    # PASO 3: Hacer petición POST /propietarios/
    # ============================================
    # client.post() simula un usuario haciendo POST
    # json=propietario_payload envía los datos en formato JSON
    # Esto es EQUIVALENTE a:
    #   curl -X POST http://localhost:8000/propietarios/ \
    #        -H "Content-Type: application/json" \
    #        -d '{"nombre": "Ana", ...}'
    response_propietario = client.post("/propietarios/", json=propietario_payload)
    
    # ============================================
    # PASO 4: Verificar que se creó correctamente (status 201)
    # ============================================
    # 201 = Created (éxito, recurso creado)
    assert response_propietario.status_code == 201
    # ✅ Si retorna 201: correcto
    # ❌ Si retorna 400/404/500: error, test falla
    
    # ============================================
    # PASO 5: Extraer datos de la respuesta
    # ============================================
    # response_propietario.json() convierte la respuesta en diccionario Python
    # Resultado: {id: 1, nombre: "Ana", email: "usuario-a1b2c3d4e5f6@mail.com", ...}
    propietario = response_propietario.json()
    
    # ============================================
    # PASO 6: Verificar que los datos se guardaron correctamente
    # ============================================
    # Comparar: el email que enviamos == el email que retorna la API
    assert propietario["email"] == email
    # ✅ Si el email es igual: datos guardados correctamente
    # ❌ Si son diferentes: algo salió mal en la BD

    # ============================================
    # PASO 7: Preparar datos de la MASCOTA
    # ============================================
    # Ahora vamos a crear una mascota para el propietario
    # Nota: propietario["id"] es el ID del propietario creado arriba
    mascota_payload = {
        "nombre": "Luna",
        "especie": "gato",
        "raza": "Persa",
        "edad": 3,
        "propietario_id": propietario["id"],  # ← Usar el ID generado
    }

    # ============================================
    # PASO 8: Hacer petición POST /mascotas/
    # ============================================
    # Crear la mascota para el propietario
    response_mascota = client.post("/mascotas/", json=mascota_payload)
    
    # ============================================
    # PASO 9: Verificar que se creó (status 201)
    # ============================================
    assert response_mascota.status_code == 201
    # ✅ Si 201: mascota creada
    # ❌ Si error: test falla
    
    # ============================================
    # PASO 10: Extraer datos de la mascota creada
    # ============================================
    mascota = response_mascota.json()
    # mascota = {id: 1, nombre: "Luna", especie: "gato", propietario_id: 1, ...}
    
    # ============================================
    # PASO 11: Verificar datos de la mascota
    # ============================================
    # Verificar que el nombre sea "Luna"
    assert mascota["nombre"] == "Luna"
    
    # Verificar que la mascota esté vinculada al propietario correcto
    # (propietario_id debe ser igual al ID del propietario creado)
    assert mascota["propietario_id"] == propietario["id"]
    # ✅ Si ambas verificaciones pasan: TODO FUNCIONA CORRECTAMENTE


# ============================================
# TEST 3: Intentar crear mascota con propietario que NO existe (manejo de errores)
# ============================================
def test_crear_mascota_con_propietario_inexistente_devuelve_404():
    """
    Verifica que la API RECHAZA intentos de crear mascotas para propietarios inexistentes.
    
    ¿Por qué es importante?
    - Un buen API debe validar datos y retornar ERRORES apropiados
    - Si alguien intenta crear mascota para propietario_id=999999 (no existe)
    - La API debe retornar error 404 con mensaje claro
    
    Este test verifica el MANEJO DE ERRORES, no el caso exitoso.
    """
    
    # ============================================
    # PASO 1: Intentar crear mascota con propietario INEXISTENTE
    # ============================================
    # Intentamos crear una mascota pero con propietario_id=999999
    # Este propietario NO existe en la BD
    response = client.post(
        "/mascotas/",
        json={
            "nombre": "Nube",
            "especie": "perro",
            "raza": "Labrador",
            "edad": 2,
            "propietario_id": 999999,  # ← Este propietario NO existe
        },
    )

    # ============================================
    # PASO 2: Verificar que retorna ERROR 404
    # ============================================
    # 404 = Not Found (el propietario no existe)
    # Si retorna 404, significa que el API está validando correctamente
    assert response.status_code == 404
    # ✅ Si 404: Validación correcta, API rechazó la petición
    # ❌ Si 201/200: ERROR, debería haber rechazado
    
    # ============================================
    # PASO 3: Verificar mensaje de error
    # ============================================
    # response.json()["detail"] obtiene el mensaje de error
    # Debe decir exactamente: "Propietario no encontrado"
    assert response.json()["detail"] == "Propietario no encontrado"
    # ✅ Si el mensaje es correcto: El error está bien documentado
    # ❌ Si es diferente: El API no está retornando el mensaje esperado
    
    # ============================================
    # CONCLUSIÓN DEL TEST
    # ============================================
    # Si ambas verificaciones pasan:
    # ✅ El API valida datos correctamente
    # ✅ Rechaza peticiones inválidas con código 404
    # ✅ Proporciona mensajes de error claros
