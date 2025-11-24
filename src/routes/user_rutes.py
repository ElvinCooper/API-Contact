from flask import Blueprint, request, jsonify
from src.modelos.users import Usuario
from src.schemas.user_schema import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.extensions import db
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow.exceptions import ValidationError
#from utils.mailer import send_simple_email_message



usuario_bp = Blueprint('usuarios', __name__)
usuario_schema = UserSchema()
usuarios_schema = UserSchema(many=True)


# Enpoint para registrar usuarios 
@usuario_bp.route('/register', methods=['POST'])
def create_usuario():
    """
    Registro de usuario
    """ 
    try:
        json_data = request.get_json()
        username = json_data.get('username')
        password = json_data.get('password')
        email    = json_data.get('email')

        # verificar si existe username, password e email en la solicitud
        if not username or not password:
            return jsonify({"mensaje": "Username y Password son requeridos"}), 400
        
        # validacion de duplicados
        if Usuario.query.filter_by(username=username).first():
            return jsonify({"mensaje": "Ya existe un usuario con este username"}), 400
        
        if Usuario.query.filter_by(username=email).first():
            return jsonify({"mensaje": "Ya existe un usuario con este email"}), 400
        
        # creacion del usuario
        nuevo_usuario = Usuario(username = username,
                                password=generate_password_hash(password),
                                email=email)
        
                
        db.session.add(nuevo_usuario)
        db.session.commit()


        # Logica de envio de correo
      #   send_simple_email_message(
      #       to_email=email,
      #      subject='Bienvenido a la api contacto',
      #      template_name= 'register'
      #  )        

        return jsonify(usuario_schema.dump(nuevo_usuario)), 201
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400




# Enpoint para login 
@usuario_bp.route('/login', methods=['POST'])
def login():
    """
    Login de usuario

    Este enpoint permite al usuario loguearse para obtener su token
    y poder acceder a la informacion de los contactos.
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: cuerpo
        required: true
        schema:
          id: LoginUsuario
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: juan123
            password:
              type: string
              example: claveSegura123
    responses:
      200:
        description: Autenticación exitosa, retorna JWT
        schema:
          properties:
            mensaje:
              type: string
            access_token:
              type: string
      401:
        description: Credenciales inválidas
      404:
        description: Usuario no encontrado
    """
    data     = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Buscar el usuario en la BD
    usuario = Usuario.query.filter_by(username=username).first()
    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    # Verificar password hasheada
    if not check_password_hash(usuario.password, password):
        return jsonify({"mensaje": "Credenciales invalidas"}), 401
    
    # Generar JWT
    acces_token = create_access_token(identity=usuario.id, expires_delta=timedelta(hours=2))

    # envio de correo 
    send_simple_email_message(
           to_email=usuario.email,
           subject='Inicio de sesion en la API Contactos',
           template_name= 'login'
      ) 

    return jsonify({ "mensaje": "login exitoso",
                     "access_token": acces_token
                    }), 200




 # Enpoint para obtener el usuario logueado
@usuario_bp.route('/me', methods=['GET'])
@jwt_required()
def obtener_usuario_autenticado():
    """
    Obtener usuario autenticado

    Este endpoint permite un usuario autenticado consultar 
    la informacion del usuario que esta logueado en ese momento.
    ---
    tags:
      - Usuarios
    security:
      - BearerAuth: []
    responses:
      200:
        description: Datos del usuario autenticado
        schema:
          id: Usuario
          properties:
            id:
              type: integer
            username:
              type: string
      404:
        description: Usuario no encontrado
    """    
    user_id = get_jwt_identity()  # Extrae el 'identity' del JWT
    usuario = Usuario.query.filter_by(id=user_id).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario_schema.dump(usuario)), 200





