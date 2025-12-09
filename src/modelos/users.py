import uuid
from src.extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id      = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email    = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- Métodos de Contraseña ---

    def set_password(self, password):
        """Genera y guarda el hash de la contraseña."""
        # Se puede llamar en el constructor o en la actualización
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica una contraseña de texto plano contra el hash guardado."""
        # Compara el hash en la DB (self.password_hash) con el texto plano provisto
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Usuario {self.username}>"