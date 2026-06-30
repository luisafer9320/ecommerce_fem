import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_and_get_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create
        response = await ac.post("/products/", json={"name":"Test","price":9.99})
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == 'Test'
        pid = data['id']

        # get
        response = await ac.get(f"/products/{pid}")
        assert response.status_code == 200
        data2 = response.json()
        assert data2['id'] == pid

        # update
        response = await ac.put(f"/products/{pid}", json={"price":10.5})
        assert response.status_code == 200
        assert response.json()['price'] == 10.5

        # delete
        response = await ac.delete(f"/products/{pid}")
        assert response.status_code == 204

        # not found
        response = await ac.get(f"/products/{pid}")
        assert response.status_code == 404
