from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200


def test_crear_propietario_y_mascota():
    email = f"usuario-{uuid4().hex}@mail.com"

    propietario_payload = {
        "nombre": "Ana",
        "apellido": "Pérez",
        "email": email,
        "telefono": "600123456",
        "direccion": "Calle Mayor 1",
    }

    response_propietario = client.post("/propietarios/", json=propietario_payload)
    assert response_propietario.status_code == 201
    propietario = response_propietario.json()
    assert propietario["email"] == email

    mascota_payload = {
        "nombre": "Luna",
        "especie": "gato",
        "raza": "Persa",
        "edad": 3,
        "propietario_id": propietario["id"],
    }

    response_mascota = client.post("/mascotas/", json=mascota_payload)
    assert response_mascota.status_code == 201
    mascota = response_mascota.json()
    assert mascota["nombre"] == "Luna"
    assert mascota["propietario_id"] == propietario["id"]


def test_crear_mascota_con_propietario_inexistente_devuelve_404():
    response = client.post(
        "/mascotas/",
        json={
            "nombre": "Nube",
            "especie": "perro",
            "raza": "Labrador",
            "edad": 2,
            "propietario_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Propietario no encontrado"
