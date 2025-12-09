# from .test_contactos_crud import registrar_y_loguear_usuario
# import uuid
#
#
# def test_crear_contacto(client):
#     headers = registrar_y_loguear_usuario(client)  # Obténer el token
#     response = client.post('/api/contactos', json={
#         "nombre": "Test User",
#         "email": "test@example.com",
#         "telefono": "123456789"
#     }, headers=headers)
#     assert response.status_code in (200, 201)
#
#
#
# def test_swagger_endpoint(client):
#     response = client.get('/apispec_1.json')
#     assert response.status_code == 200
#     assert 'swagger' in response.get_json()  # Verifica que la respuesta incluye la spec de Swagger
#
#
#
#
# def test_crear_contacto_email_invalido(client):
#     headers = registrar_y_loguear_usuario(client)
#     response = client.post('/api/contactos', json={
#         "nombre": "Test User",
#         "email": "email_invalido",
#         "telefono": "123456789"
#     }, headers=headers)
#     assert response.status_code == 400
#
#
#
# def test_crear_contacto_datos_faltantes(client):
#     headers = registrar_y_loguear_usuario(client)
#     response = client.post('/api/contactos', json={
#         "nombre": "Test User"
#         # Falta email
#     }, headers=headers)
#     assert response.status_code == 400
#
#
#
# def test_obtener_contacto_no_existente(client):
#     headers = registrar_y_loguear_usuario(client)
#     response = client.get('/api/contactos/9999', headers=headers)
#     assert response.status_code == 404
#
#
#
# def test_actualizar_contacto_no_existente(client):
#     headers = registrar_y_loguear_usuario(client)
#     response = client.put('/api/contactos/9999', json={
#         "nombre": "Contacto Actualizado"
#     }, headers=headers)
#     assert response.status_code == 404
#
#
#
# def test_eliminar_contacto_no_existente(client):
#     headers = registrar_y_loguear_usuario(client)
#     response = client.delete('/api/contactos/9999', headers=headers)
#     assert response.status_code == 400
#
#
#
# def test_registro_usuario_existente(client):
#     username = f"testuser_{uuid.uuid4()}"
#     email = f"test_{uuid.uuid4()}@example.com"
#     client.post('/api/register', json={
#         "username": username,
#         "password": "testpass",
#         "email": email
#     })
#     response = client.post('/api/register', json={
#         "username": username,
#         "password": "testpass",
#         "email": email
#     })
#     assert response.status_code == 400
#
#
# def test_login_credenciales_invalidas(client):
#     response = client.post('/api/login', json={
#         "username": "noexiste",
#         "password": "incorrecta"
#     })
#     assert response.status_code == 404
#
#
#
#
# def test_registro_datos_faltantes(client):
#     response = client.post('/api/register', json={
#         "username": "testuser"
#         # Falta password y email
#     })
#     assert response.status_code == 400
#
#
#
#
# def test_login_password_incorrecta(client):
#     username = f"testuser_{uuid.uuid4()}"
#     email = f"test_{uuid.uuid4()}@example.com"
#     client.post('/api/register', json={
#         "username": username,
#         "password": "testpass",
#         "email": email
#     })
#     response = client.post('/api/login', json={
#         "username": username,
#         "password": "incorrecta"
#     })
#     assert response.status_code == 401