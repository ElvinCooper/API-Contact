from src.modelos.contacts import Contacto 
from src.modelos.users import Usuario
import uuid

def test_usuario_model(db):   
    unique_username = f"testuser_{uuid.uuid4()}" 
    unique_email = f"test_{uuid.uuid4()}@example.com"  
    usuario = Usuario(username=unique_username, password="testpass", email=unique_email)
    db.session.add(usuario)
    db.session.commit()
    assert usuario.id is not None
    assert Usuario.query.filter_by(username=unique_username).first() == usuario
    assert str(usuario) == f"<Usuario {unique_username}>"



def test_contacto_model(db):
    unique_email = f"test_{uuid.uuid4()}@example.com"  
    contacto = Contacto(nombre="Test", email=unique_email, telefono="123456789")
    db.session.add(contacto)
    db.session.commit()
    assert contacto.id is not None
    assert Contacto.query.filter_by(email=unique_email).first() == contacto
    assert str(contacto) == "<Contact Test>"



def test_contacto_repr(db):
    unique_email = f"test_{uuid.uuid4()}@example.com"
    contacto = Contacto(nombre="Test", email=unique_email, telefono="123456789")
    db.session.add(contacto)
    db.session.commit()
    assert str(contacto)  # Prueba __repr__ si está definido    




def test_contacto_email_validation(db):
    contacto = Contacto(nombre="Test", email="invalid_email", telefono="123456789")
    db.session.add(contacto)
    try:
        db.session.commit()
        assert False, "Debería fallar por email inválido"
    except:
        db.session.rollback()    