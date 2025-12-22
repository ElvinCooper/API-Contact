from http import HTTPStatus


def test_crear_categoria(client, auth_headers):

    # registrar un pais
    create_resp = client.post('/api/v1/pais/register', json={"nombre_pais": "pais example",
                                                             "codigo_iso": "do"},
                                                             headers=auth_headers)
    assert create_resp.status_code  == 201


def test_registrar_pais_duplicado(client, sample_pais ,auth_headers):
    create_resp = client.post('/api/v1/pais/register', json={"nombre_pais": "Republica Dominicana",
                                                             "codigo_iso": "do"},
                                                       headers=auth_headers)
    assert create_resp.status_code == HTTPStatus.CONFLICT


def test_registrar_pais_sin_token(client, auth_headers):
    create_resp = client.post('/api/v1/pais/register', json={"nombre_pais": "mexico",
                                                             "codigo_iso": "do"})
    assert create_resp.status_code == HTTPStatus.UNAUTHORIZED


def test_consultar_pais_por_id(client, auth_headers, pais_id):
    create_resp = client.get(f'/api/v1/pais/{pais_id}', headers=auth_headers)

    assert create_resp.status_code == HTTPStatus.OK


def test_consultar_pais_inexistente(client, auth_headers):
    create_resp = client.get('/api/v1/pais/gfgh5f584', headers=auth_headers)

    assert create_resp.status_code == HTTPStatus.NOT_FOUND


def test_actualiza_pais(client, auth_headers, pais_id):

    put_resp = client.put(f'/api/v1/pais/update/{pais_id}',
                          json={"nombre_pais": "pais actualizado"},
                          headers=auth_headers)
    assert put_resp.status_code == 200
    assert put_resp.get_json()["nombre_pais"] == "pais actualizado"


def test_eliminar_pais(client, auth_headers, pais_id):

    del_resp = client.delete(f'/api/v1/pais/delete/{pais_id}', headers=auth_headers)
    assert del_resp.status_code == 204

    # Confirmar que ya no existe
    get_deleted = client.get(f'/api/v1/pais/{pais_id}', headers=auth_headers)
    assert get_deleted.status_code == 404