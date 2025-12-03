import pytest
from src.run import create_app
from src.extensions import db as _db
import os
from src.modelos.users import Usuario
from src.modelos.contacts import Contacto
from src.modelos.category_model import Categoria
from src.modelos.pais_model import Pais




@pytest.fixture(scope='session')
def app():
    """
    Crear la aplicacion para testing.

    """

    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')

    # Usar variable de entorno del workflow o valor por defecto para Docker local
    test_db_uri = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        "postgresql://test_user:test_password@test-db:5432/test_contact"  # Local Docker
    )

    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_db_uri,  # ← Usar variable
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key-do-not-use-in-production',
        'WTF_CSRF_ENABLED': False,
        'RATELIMIT_ENABLED': False
    })

    # crear todas las tablas.
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def db(app):
    """
    Proporciona una sesión de base de datos limpia para cada test.

    scope='function': Se ejecuta antes de CADA test individual
    Esto asegura que cada test comience con una BD vacía
    """
    with app.app_context():
        # Limpiar todas las tablas antes del test
        _db.session.remove()
        _db.drop_all()
        _db.create_all()

        yield _db

        # Rollback después del test
        _db.session.remove()


@pytest.fixture
def client(app):
    """
    Cliente de prueba para hacer peticiones HTTP a la API.

    Uso:
        response = client.get('/api/v1/auth/register')
        response = client.post('/api/v1/auth/register', json={...})
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Runner para comandos CLI de Flask.

    Uso:
        result = runner.invoke(args=['db', 'init'])
    """
    return app.test_cli_runner()



# ============================================
# FIXTURES DE DATOS DE PRUEBA
# ============================================

@pytest.fixture
def sample_user(db):
    """
    Crea un usuario de ejemplo en la BD.

    """
    user = Usuario(
        username='testuser',
        email='test@example.com'
    )

    user.set_password('testpassword')

    db.session.add(user)
    db.session.commit()
    return user



@pytest.fixture
def sample_category(db):
    """
    Crea una categoría de ejemplo.
    """
    category = Categoria(
        nombre_categoria='Electronics'
    )
    db.session.add(category)
    db.session.commit()
    return category



@pytest.fixture
def sample_pais(db):
    """
    Crea un pais de ejemplo.
    """
    pais = Pais(
        nombre_pais= "Republica Dominicana",
        codigo_iso= "DO"
    )
    db.session.add(pais)
    db.session.commit()
    return pais



@pytest.fixture
def sample_contacto(db):
    """
    Crea un contacto de ejemplo.
    """
    contact = Contacto(
        nombre= "test_contact",
        email= "contactotest@gmail.com",
        telefono="8296451276"
    )
    db.session.add(contact)
    db.session.commit()
    return contact



@pytest.fixture
def auth_token(client, sample_user):
    """
    Obtiene un token JWT válido para autenticación.
    """

    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    if response.status_code == 200:
        data = response.get_json()
        return data.get('access_token')

    print(f"\n--- DEBUG: Login falló en auth_token, Status: {response.status_code} ---")
    print(f"--- DEBUG: Respuesta: {response.get_data(as_text=True)} ---")

    return None



@pytest.fixture
def auth_headers(auth_token):
    """
    Headers con autenticación para peticiones protegidas.

    Uso:
        response = client.get('/api/protected', headers=auth_headers)
    """
    if auth_token:
        return {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
    return {'Content-Type': 'application/json'}