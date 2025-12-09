# import pytest
# from src.run import create_app
#
# @pytest.fixture
# def client():
#     app = create_app()
#     app.config.from_object('config.TestingConfig')
#     with app.test_client() as client:
#         yield client
#
# def test_cors_headers(client):
#     response = client.options('/api/contactos')
#     assert response.status_code == 200
#     assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'
#     assert 'GET, POST, PUT, DELETE, OPTIONS' in response.headers['Access-Control-Allow-Methods']
#     assert 'Content-Type, Authorization' in response.headers['Access-Control-Allow-Headers']