from datetime import datetime, timezone
import uuid
from src.extensions import db

class Pais(db.Model):
    __tablename__ = 'pais'
    
    pais_id      = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_pais  = db.Column(db.String(100), nullable=False)    
    codigo_iso   = db.Column(db.String(2), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    contactos = db.relationship("src.modelos.contacts.Contacto", back_populates="pais")