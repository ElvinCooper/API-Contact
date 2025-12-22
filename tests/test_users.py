from http import HTTPStatus


def test_registrar_usuario(client):
    create_resp = client.post('/api/v1/auth/register', json={"username":"user example",
                                                             "email":"email@example.com",
                                                             "password": "test1234"})
    assert create_resp.status_code == 201


def test_registrar_user_con_email_duplicad(client, sample_user):
    create_resp = client.post('/api/v1/auth/register', json={"username": "another user",
                                                             "email": "test@example.com",
                                                             "password": "test1234"
                                                             })
    assert create_resp.status_code == HTTPStatus.CONFLICT




# def test_consultar_usuario_por_id(client, auth_headers, user_id):
#     create_resp = client.get(f'/api/v1/usuario/{user_id}', headers=auth_headers)
#
#     assert create_resp.status_code == HTTPStatus.OK


# def test_consultar_categoria_inexistente(client, auth_headers):
#     create_resp = client.get('/api/v1/categoria/gfgh5684', headers=auth_headers)
#
#     assert create_resp.status_code == HTTPStatus.NOT_FOUND
#
#
# def test_actualiza_categoria(client, auth_headers, categoria_id):
#
#     put_resp = client.put(f'/api/v1/categoria/update/{categoria_id}',
#                           json={"nombre_categoria": "Categoria Actualizada"},
#                           headers=auth_headers)
#     assert put_resp.status_code == 200
#     assert put_resp.get_json()["nombre_categoria"] == "Categoria Actualizada"
#
#
# def test_eliminar_categoria(client, auth_headers, categoria_id):
#
#     del_resp = client.delete(f'/api/v1/categoria/delete/{categoria_id}', headers=auth_headers)
#     assert del_resp.status_code in (200, 204)
#
#     # Confirmar que ya no existe
#     get_deleted = client.get(f'/api/v1/categoria/{categoria_id}', headers=auth_headers)
#     assert get_deleted.status_code == 404