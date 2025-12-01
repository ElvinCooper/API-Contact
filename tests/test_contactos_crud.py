

def registrar_y_loguear_usuario(client):
    # Crear usuario
    client.post('/api/register', json={
        "username": "testuser",
        "password": "testpass",
        "email": "testuser@example.com"
    })

    # Loguear usuario
    login_resp = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })

    token = login_resp.get_json()['access_token']
    return {"Authorization": f"Bearer {token}"}


def test_crud_contacto(client):
    headers = registrar_y_loguear_usuario(client)

    # Crear contacto
    create_resp = client.post('/api/contactos', json={
        "nombre": "Contacto Test",
        "email": "contacto@test.com",
        "telefono": "123456789"
    }, headers=headers)
    assert create_resp.status_code in (200, 201)
    contacto = create_resp.get_json()
    contacto_id = contacto["id"]

    # Obtener contacto
    get_resp = client.get(f'/api/contactos/{contacto_id}', headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.get_json()["nombre"] == "Contacto Test"

    # Actualizar contacto
    put_resp = client.put(f'/api/contactos/{contacto_id}', json={
        "nombre": "Contacto Actualizado"
    }, headers=headers)
    assert put_resp.status_code == 200
    assert put_resp.get_json()["nombre"] == "Contacto Actualizado"

    # Eliminar contacto
    del_resp = client.delete(f'/api/contactos/{contacto_id}', headers=headers)
    assert del_resp.status_code in (200, 204)

    # Confirmar que ya no existe
    get_deleted = client.get(f'/api/contactos/{contacto_id}', headers=headers)
    assert get_deleted.status_code == 404
