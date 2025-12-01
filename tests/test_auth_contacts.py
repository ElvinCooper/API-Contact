
def test_crear_contacto_autenticado(client):
    # 1. Registrar usuario
    registro_resp = client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass",
        "email": "testuser@example.com"
    })
    assert registro_resp.status_code in (200, 201)

    # 2. Login para obtener el token
    login_resp = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert login_resp.status_code == 200
    token = login_resp.get_json()['access_token']
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 3. Crear contacto usando el token
    contacto_resp = client.post('/api/contactos', json={
        "nombre": "Test Contact",
        "email": "contact@example.com",
        "telefono": "123456789"
    }, headers=headers)

    assert contacto_resp.status_code in (200, 201)
    data = contacto_resp.get_json()
    assert data["nombre"] == "Test Contact"
    assert data["email"] == "contact@example.com"
