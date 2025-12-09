"""
Tests para autenticación y autorización.
"""
from http import HTTPStatus
import pytest
from werkzeug.security import check_password_hash
import time

#pytestmark = pytest.mark.integration


class TestAuthentication:
    # """Tests para login y registro"""

    def test_register_user(self, client):
        """Test: Registrar un nuevo usuario"""
        new_user = {
            "username": "newuser",
            "email": 'newuser@example.com',
            "password": "newpassword"
        }

        response = client.post('/api/v1/auth/register', json=new_user)

        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['username'] == 'newuser'


    def test_register_duplicate_email(self, client, sample_user):
        """Test: No se puede registrar email duplicado"""
        duplicate_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = client.post('/api/v1/auth/register', json=duplicate_user)

        assert response.status_code == 409

    def test_login_success(self, client, sample_user):
        """Test: Login exitoso"""
        credentials = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        response = client.post('/api/v1/auth/login', json=credentials)

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data


    def test_login_wrong_password(self, client, sample_user):
        """Test: Login con contraseña incorrecta"""
        credentials = {
            'email': 'test@example.com',
            'password': 'testpassword22'
        }

        response = client.post('/api/v1/auth/login', json=credentials)

        assert response.status_code == 401


    def test_login_nonexistent_email(self, client):
        """Test: Login con email que no existe"""
        credentials = {
            'email': 'nonexistent@gmail.com',
            'password': 'testpassword22'
        }

        response = client.post('/api/v1/auth/login', json=credentials)

        assert response.status_code == 401


class TestAuthorization:
    """Tests para protección de endpoints"""

    def test_protected_endpoint_without_token(self, client):
        """Test: Acceder a endpoint protegido sin token"""
        response = client.post('/api/v1/categoria/register', json={
            "nombre_categoria": "Cafe Santo domingo"
        })

        # Debe rechazar sin autenticación
        assert response.status_code in [401, 403]

    def test_protected_endpoint_with_valid_token(self, client, auth_headers, sample_category):
        """Test: Acceder a endpoint protegido con token válido"""
        new_category = {
            "nombre_categoria": "Categoria valida"
        }

        response = client.post(
            '/api/v1/categoria/register',
            json=new_category,
            headers=auth_headers
        )

        assert response.status_code == 201

    def test_protected_endpoint_with_invalid_token(self, client, sample_category):
        """Test: Acceder con token inválido"""
        invalid_headers = {
            'Authorization': 'Bearer invalid_token_here',
            'Content-Type': 'application/json'
        }

        response = client.post(
            '/api/v1/categoria/register',
            json={'nombre_categoria': 'TestCat'},
            headers=invalid_headers
        )

        assert response.status_code in [401, 422]