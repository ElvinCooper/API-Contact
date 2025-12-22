import pytest
from src.run import create_app
from src.extensions import db as _db
import os
from src.modelos.users import Usuario
from src.modelos.contacts import Contacto
from src.modelos.category_model import Categoria
from src.modelos.pais_model import Pais
import time
import psycopg2


@pytest.fixture(scope='session')
def app():
    """Crear la aplicación para testing."""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')

    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': "postgresql://test_user:test_password@test-db:5432/test_contact",
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 5,
            'max_overflow': 0,
            'connect_args': {
                'connect_timeout': 10  # Timeout de conexión
            }
        },
        'JWT_SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
        'RATELIMIT_ENABLED': False
    })

    # Reintentar si falla la conexión
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with app.app_context():
                # Verificar conexión
                _db.engine.connect()
                print(f" Conectado a BD en intento {attempt + 1}")

                _db.drop_all()
                _db.create_all()
                print(" Tablas creadas exitosamente")
                break
        except psycopg2.OperationalError as e:
            print(f" Intento {attempt + 1}/{max_retries} falló: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Esperar antes de reintentar
            else:
                raise

    yield app

    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.engine.dispose()


@pytest.fixture(scope='function', autouse=True)  # autouse: se ejecuta siempre
def db(app):
    """Proporciona una sesión limpia para cada test."""
    with app.app_context():
        # TRUNCATE es más rápido y no causa deadlocks
        meta = _db.metadata
        for table in reversed(meta.sorted_tables):
            _db.session.execute(_db.text(f'TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;'))
        _db.session.commit()

        yield _db

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
def categoria_id(client, auth_headers):
    # registrar una nueva categoria
    create_resp = client.post('/api/v1/categoria/register', json={"nombre_categoria": "categoria example"},
                              headers=auth_headers)
    categoria = create_resp.get_json()
    return categoria["id_categoria"]



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
def pais_id(client, auth_headers):
    create_resp = client.post('/api/v1/pais/register', json={"nombre_pais": "pais2 example",
                                                             "codigo_iso": "DO"},
                                                       headers=auth_headers)
    pais = create_resp.get_json()
    return pais["pais_id"]



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