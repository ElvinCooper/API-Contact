from flask import Flask
from flask_cors import CORS
from src.config import DevelopmentConfig, ProductionConfig, TestingConfig
from src.extensions import db, init_extensions, migrate
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_smorest import Api
from src.routes.contact_rutes import contacto_bp
from src.routes.user_rutes import  usuario_bp
from src.routes.category_rutes import categoria_bp
from src.routes.pais_rutes import pais_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address




def create_app(env=None): 
    
    load_dotenv()    

    # detectar el entorno desde .FLASKENV
    env = os.getenv("FLASK_ENV", "DEVELOPMENT")
    print(f"El entorno es {env}")  # temporal para debug.
    
    app = Flask(__name__)

    if env == "DEVELOPMENT":
        app.config.from_object(DevelopmentConfig)
    elif env == "production":    
        app.config.from_object(ProductionConfig)
        
    else:
        app.config.from_object(TestingConfig) 


    # ----------------------------------------------------
    # PASO 1: CONFIGURACIÓN DE REDIS PARA RATE LIMITER
    # ----------------------------------------------------
    
    #REDIS_URL = os.environ.get("RATELIMIT_STORAGE_URL")
    
    # if env == "production" and not REDIS_URL:
    #     # En producción (Render), el Rate Limiter es obligatorio.
    #     raise EnvironmentError("FATAL: RATELIMIT_STORAGE_URL no está configurada. Necesita Upstash Redis en Render.")
    
    # if REDIS_URL:
    #     # Usar Redis para el almacenamiento de límites de velocidad.
    #     STORAGE_URI = REDIS_URL
    #     print(f"Limiter usará Redis en: {STORAGE_URI.split('@')[-1]}")
    # else:
    #     # En desarrollo, si no está configurado, usa la memoria local (solo para pruebas).
    #     STORAGE_URI = "memory://"
    #     print("ADVERTENCIA: Usando Rate Limiting en memoria (solo para desarrollo).")

    # ----------------------------------------------------
    # PASO 2: INICIALIZACIÓN DE FLASK-LIMITER
    # ----------------------------------------------------

    # limiter = Limiter(
    #     storage_uri=STORAGE_URI,
    #     # Usar la IP remota para identificar al cliente.
    #     key_func=get_remote_address,
    #     # Límite predeterminado (se aplicará a todas las rutas que no tengan uno explícito)
    #     default_limits=["200 per day", "50 per hour"]
    # )
    
    # limiter.init_app(app)

    # Opcional: Personalizar la respuesta 429 "Too Many Requests"
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Límite de Solicitudes Excedido (429)",
            "message": "Ha enviado demasiadas solicitudes en el tiempo permitido. Intente nuevamente más tarde."
        }), 429


    # # Inicializar CORS para permitir solicitudes desde el frontend
    # frontend_url = app.config.get('FRONTEND_URL', 'http://localhost:3000')  # Valor por defecto
    # if not frontend_url:
    #     raise ValueError("FRONTEND_URL debe estar definido en la configuración.")
    
    # # Inicializar CORS para permitir solicitudes desde el frontend
    # CORS(app, resources={r"/api/*": {"origins": frontend_url,
    #     "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #     "allow_headers": ["Content-Type", "Authorization"],
    #     "supports_credentials": True
    # }})

    # Iniciando las extensiones
    init_extensions(app)
    migrate = Migrate(app, db) 
   
    api = Api(app)
    
    # codigo para ejecutar migraciones, solo en production  
    #=====================================#
    
    #=====================================#
    
            
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise ValueError(f"SQLALCHEMY_DATABASE_URI no está configurado para el entorno: {env}")            
    
    # Registro de blueprints    
    api.register_blueprint(contacto_bp, url_prefix='/api/v1')
    api.register_blueprint(usuario_bp , url_prefix='/api/v1')
    api.register_blueprint(categoria_bp , url_prefix='/api/v1')
    api.register_blueprint(pais_bp , url_prefix='/api/v1')
    
   # ----------------------------------------------------
    # PASO 3: Ejemplo de Límite en una Ruta.
    # ----------------------------------------------------
    
    
    @app.route('/', methods=['GET'])
    @limiter.exempt  # Excluir el home del límite predeterminado.
    def home():
        return "<h1> Bienvenido </h1>"


    return app


app = create_app()



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)







