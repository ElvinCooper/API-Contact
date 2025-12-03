from src.modelos.contacts import Contacto 
from src.modelos.users import Usuario
from src.modelos.category_model import Categoria
from src.modelos.contacts import Contacto
from src.modelos.pais_model import Pais
from werkzeug.security import generate_password_hash, check_password_hash
import pytest
import uuid



class TestCategoryModel:
    """Tests para el modelo Categoria"""

    def test_create_category(self, db):
        """Test: Crear una categoría"""
        category = Categoria(
            nombre_categoria='Furniture'
        )
        db.session.add(category)
        db.session.commit()

        assert category.id_categoria is not None
        assert category.nombre_categoria == 'Furniture'


    def test_category_unique_name(self, client, auth_headers, sample_category):
        """Test: Los nombres de categoría deben ser únicos"""

        duplicate_category = {
            "nombre_categoria":"Electronics"
        }

        response = client.post("/api/v1/categoria/register",
                               json=duplicate_category,
                               headers=auth_headers)

        assert response.status_code == 409


class TestUserModel:
    """Tests para el modelo Usuario"""

    def test_create_user(self, db):
        """Test: Crear un usuario"""
        user = Usuario(
            username='newuser',
            email='new@example.com',
            password=generate_password_hash('testnewuser')
        )
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'new@example.com'

    def test_password_hashing(self, sample_user):
        """Test: Las contraseñas deben estar hasheadas"""

        assert sample_user.password != 'testpassword'
        assert sample_user.check_password('testpassword') is True