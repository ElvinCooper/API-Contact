from datetime import datetime, timezone
import uuid
from src.extensions import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id_categoria             = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_categoria         = db.Column(db.String(100), nullable=False)    
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    contactos = db.relationship("src.modelos.contacts.Contacto", back_populates="categoria")        