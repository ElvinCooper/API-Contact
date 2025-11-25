from flask import jsonify
from flask_smorest import abort as smorest_abort, Blueprint
from src.modelos.users import Usuario
from src.schemas.user_schema import UserSchema, UserSimpleSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.extensions import db
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow.exceptions import ValidationError
from flask.views import MethodView 
from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from flask import jsonify, current_app, response
import traceback

#from utils.mailer import send_simple_email_message



usuario_bp = Blueprint('usuarios', __name__, description="Operaciones con usuarios")



@usuario_bp.route('/usuarios')
class UsuarioRegister(MethodView):
  @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema(many=True))
  # @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  #@usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self):
      """
      Listar todos los contactos

      En este endpoint un usuario autenticado puede listar todos
      los contactos existentes en la base de datos.
      """    
      list_users = Usuario.query.all()    
      
      return list_users, HTTPStatus.OK
      
      return jsonify(contacts_schema.dump(list_contacts))



# Endpoint para consultar un contacto con su id
@usuario_bp.route('/usuario/<string:id_usuario>')
class UserResourceId(MethodView):
  @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)
    #@usuario_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ErrorSchema, description="Usuario no encontrado", example={"succes": False, "message": "Usuario no encontrado"})
    #@usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
    #@jwt_required()
  def get(self, id_usuario):
      """
      Obtener contacto por ID

      Este endpoint permite al usuario obtener los datos de un contacto por su respectivo id.
      """    
      contacto = Usuario.query.filter_by(id_usuario=id_usuario).first()
      if not contacto:
        smorest_abort(HTTPStatus.NOT_FOUND, description="Contacto no encontrado")
            
      return jsonify(contacto(contacto)), HTTPStatus.OK    



# Enpoint para insertar un contacto
@usuario_bp.route('/auth/register')
class UserRegisterResource(MethodView):
    #@limiter.limit("5 per minute")  # intentos por minuto
    #@usuario_bp.arguments(UserRegisterSchema)
    #@usuario_bp.response(HTTPStatus.CREATED, UserResponseSchema)
    #@usuario_bp.alt_response(HTTPStatus.CONFLICT, schema=ErrorSchema, description="Ya existe un usuario con ese email", example={"success": False, "message": "Ya existe un usuario con ese email"})
    #@usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  def post(self, user_data):
      """
      Crear nuevo contacto en la base de datos.

      Este endpoint permite a un usuario autenticado crear un nuevo contacto
      proporcionando nombre, email y teléfono.
      """
      try:
          if Usuario.query.filter_by(email=user_data['email']).first():
            smorest_abort(HTTPStatus.CONFLICT, message=f"Ya existe un usuario con ese email")
                
           # Crear el nuevo usuario
            new_user = Usuario(
                id_usuario=str(uuid.uuid4()),
                user_name=data_usuario['user_name'],
                email=data_usuario['email'],
                password=generate_password_hash(data_usuario['password'])                
            )          

          db.session.add(new_user)
          db.session.commit()

          return new_user, HTTPStatus.CREATED
       
      except HTTPException as http_exc:
        raise http_exc  # esto permite que pasen errores como 401, 400 etc...
      except Exception as e:
       current_app.logger.error(f"Error al registrar usuario: {str(e)}\n{traceback.format_exc()}")
       db.session.rollback()
       smorest_abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(e)}")
      except ValidationError as e:
          return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST





# Enpoint para login 
# @usuario_bp.route('/login', methods=['POST'])
# def login():
#     """
#     Login de usuario

#     Este enpoint permite al usuario loguearse para obtener su token
#     y poder acceder a la informacion de los contactos.
#     """
#     data     = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     # Buscar el usuario en la BD
#     usuario = Usuario.query.filter_by(username=username).first()
#     if not usuario:
#         return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
#     # Verificar password hasheada
#     if not check_password_hash(usuario.password, password):
#         return jsonify({"mensaje": "Credenciales invalidas"}), 401
    
#     # Generar JWT
#     acces_token = create_access_token(identity=usuario.id, expires_delta=timedelta(hours=2))

#     # envio de correo 
#     send_simple_email_message(
#            to_email=usuario.email,
#            subject='Inicio de sesion en la API Contactos',
#            template_name= 'login'
#       ) 

#     return jsonify({ "mensaje": "login exitoso",
#                      "access_token": acces_token
#                     }), 200




#  # Enpoint para obtener el usuario logueado
# @usuario_bp.route('/me', methods=['GET'])
# @jwt_required()
# def obtener_usuario_autenticado():
#     """
#     Obtener usuario autenticado

#     Este endpoint permite un usuario autenticado consultar 
#     la informacion del usuario que esta logueado en ese momento.
#     """    
#     user_id = get_jwt_identity()  # Extrae el 'identity' del JWT
#     usuario = Usuario.query.filter_by(id=user_id).first()

#     if not usuario:
#         return jsonify({"error": "Usuario no encontrado"}), 404

#     return jsonify(usuario_schema.dump(usuario)), 200





