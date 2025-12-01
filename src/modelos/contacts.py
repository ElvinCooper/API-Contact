from sqlalchemy import UniqueConstraint
from datetime import datetime, timezone
import uuid
from src.extensions import db

class Contacto(db.Model):
    __tablename__ = 'contactos'
    
    id_contacto             = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre         = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    telefono       = db.Column(db.String(20))
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))    
    
    # Foreign Key a categoria
    id_categoria   = db.Column(db.String(36), db.ForeignKey('categorias.id_categoria'), nullable=True)    
    # Relación con Categoria
    categoria = db.relationship("src.modelos.category_model.Categoria", back_populates="contactos")
    
    # Foreign Key a pais
    pais_id = db.Column(db.String(36), db.ForeignKey('pais.pais_id'), nullable=True)
    # Relación con Pais
    pais = db.relationship("src.modelos.pais_model.Pais", back_populates="contactos")

    __table_args__ = (
        UniqueConstraint('email', name='uq_usuarios_email'),
    )   


    def __repr__(self):
        return f"<Contact {self.nombre}>"