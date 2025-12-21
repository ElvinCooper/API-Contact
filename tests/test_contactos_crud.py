

def test_registrar_y_loguear_usuario(client):
    # Crear usuario
    client.post('/api/v1/auth/register', json={
        "username": "testuser",
        "password": "testpass",
        "email": "testuser@example.com"
    })

    # Loguear usuario
    login_resp = client.post('/api/v1/auth/login', json={
        "email": "testuser@example.com",
        "password": "testpass"
    })

    assert login_resp.status_code == 200, f"Error en login: {login_resp.get_json()}"

    token = login_resp.get_json()["access_token"]


def test_crud_contacto(client, auth_headers):
    #headers = test_registrar_y_loguear_usuario(client)

    # Crear contacto
    create_resp = client.post('/api/v1/contacto/register', json={
        "nombre": "Contacto Test",
        "email": "contacto@test.com",
        "telefono": "123456789"
    }, headers=auth_headers)
    assert create_resp.status_code in (200, 201)
    contacto = create_resp.get_json()
    contacto_id = contacto["id_contacto"]

    # # Obtener contacto
    # get_resp = client.get(f'/api/v1/contacto/{contacto_id}', headers=auth_headers)
    # assert get_resp.status_code == 200
    # assert get_resp.get_json()["nombre"] == "Contacto Test"

    #Actualizar contacto
    updated_data = {"nombre": "Contacto Actualizado"}
    put_resp = client.put(f'/api/v1/contacto/update/{contacto_id}',
                          json={"nombre": "Contacto Actualizado"},
                          headers=auth_headers)
    assert put_resp.status_code == 201
    assert put_resp.get_json()["nombre"] == "Contacto Actualizado"

#     # Eliminar contacto
    del_resp = client.delete(f'/api/v1/contacto/delete/{contacto_id}', headers=auth_headers)
    assert del_resp.status_code in (200, 204)

    # Confirmar que ya no existe
    get_deleted = client.get(f'/api/contactos/{contacto_id}', headers=auth_headers)
    assert get_deleted.status_code == 404
