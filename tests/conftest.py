import pytest
from src.run import create_app
from src.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite://:memory:',
        'TESTING': True,
        'JWT_SECRET_KEY': 'test-secret'
    }) 

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        _db.drop_all()
        _db.create_all()                
        yield _db
        _db.session.rollback()
        _db.drop_all()
    