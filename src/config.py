import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class BaseConfig:
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False     # Desactiva el seguimiento de modificaciones de objetos para ahorrar recursos
    JWT_SECRET_KEY =  os.getenv("JWT_SECRET_KEY", "default-secret")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    API_TITLE = "API Contactos"
    API_VERSION = "v1.0.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/apidocs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Ingrese su token JWT en el formato: Bearer <token>"
                }
            }
        },
        "security": [{"BearerAuth": []}]  # Aplicar globalmente
    }
 

class DevelopmentConfig(BaseConfig):
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")  
    FRONTEND_URL = "http://localhost:3000"
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI debe estar definido en desarrollo.")


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")    
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI debe estar definido en producción.")
    
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    if not FRONTEND_URL:
        raise ValueError("FRONTEND_URL debe estar definido en producción.")
    


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG=True
    RATELIMIT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI", "postgresql://test-contact:testcontact1234@localhost:5432/test-contact")
    
    
