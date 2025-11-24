import uuid
from src.extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id       = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email    = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.username}>"