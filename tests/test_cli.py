import pytest
from click.testing import CliRunner
from src.run import db
from src.modelos.users import Usuario

@pytest.fixture
def runner(app):
    return CliRunner()

def test_db_create(runner, app):
    with app.app_context():
        result = runner.invoke(app.cli.commands['db_create'])
        assert result.exit_code == 0
        assert 'Base de datos creada exitosamente' in result.output
        assert db.metadata.tables  # Verifica que las tablas existen



def test_db_drop(runner, app):
    with app.app_context():
        db.create_all()  # Crear tablas primero
        result = runner.invoke(app.cli.commands['db_drop'])
        assert result.exit_code == 0
        assert 'Base de datos eliminada' in result.output
        



def test_db_seed(runner, app):
    with app.app_context():
        db.create_all()  # Crear tablas primero
        result = runner.invoke(app.cli.commands['db.seed'])
        assert result.exit_code == 0, f"Error en db_seed: {result.exception}"
        assert 'Base de datos' in result.output
        usuario = Usuario.query.filter_by(username='Elvin').first()
        assert usuario is not None
        assert usuario.email == 'ing.elvin01cooper@gmail.com'