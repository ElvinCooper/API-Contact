from flask import jsonify
from flask_smorest import abort as smorest_abort, Blueprint
from src.modelos.users import Usuario
from src.schemas.user_schema import UserSchema, UserSimpleSchema, UserErrorSchema, UserRegisterSchema, UserResponseSchema, LogoutResponseSchema, TokenRefreshResponseSchema, UserUpdateSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from src.extensions import db
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow.exceptions import ValidationError
from flask.views import MethodView 
from http import HTTPStatus
from werkzeug.exceptions import HTTPException
from flask import jsonify, current_app
import traceback

#from utils.mailer import send_simple_email_message

usuario_bp = Blueprint('Usuarios', __name__, description="Operaciones con usuarios")


@usuario_bp.route('/usuarios')
class UsuarioRegister(MethodView):
  @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema(many=True))
  @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=UserErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self):
      """
      Listar todos los contactos

      En este endpoint un usuario autenticado puede listar todos
      los contactos existentes en la base de datos.
      """    
      list_users = Usuario.query.all()    
      
      return list_users, HTTPStatus.OK        



# Endpoint para consultar un contacto con su id
@usuario_bp.route('/usuario/<string:id_usuario>')
class UserResourceId(MethodView):
  @usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)
  @usuario_bp.alt_response(HTTPStatus.NOT_FOUND, schema=UserErrorSchema, description="Usuario no encontrado", example={"succes": False, "message": "Usuario no encontrado"})
  @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
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




@usuario_bp.route('/auth/register')
class UserRegisterResource(MethodView):
    #@limiter.limit("5 per minute")  # intentos por minuto
    @usuario_bp.arguments(UserRegisterSchema)
    @usuario_bp.response(HTTPStatus.CREATED, UserResponseSchema)
    @usuario_bp.alt_response(HTTPStatus.CONFLICT, schema=UserErrorSchema, description="Ya existe un usuario con ese email", example={"success": False, "message": "Ya existe un usuario con ese email"})
    @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
    def post(self, user_data):
      """
      Registrar nuevo contacto en la base de datos.

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




#================= Enpoint para login ======================#
@usuario_bp.route('/auth/login')
class UserRegisterResource(MethodView):
  #@limiter.limit("5 per minute")  # intentos por minuto
  @usuario_bp.arguments(UserRegisterSchema)
  @usuario_bp.response(HTTPStatus.CREATED, UserResponseSchema)
  @usuario_bp.alt_response(HTTPStatus.CONFLICT, schema=UserErrorSchema, description="Ya existe un usuario con ese email", example={"success": False, "message": "Ya existe un usuario con ese email"})
  @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  def post(self, data_login):
      """
      Login de usuario

      Este enpoint permite al usuario loguearse para obtener su token
      y poder acceder a la informacion de los contactos.
      """
      try:
        # Buscar usuario por email proveeido
        usuario = Usuario.query.filter_by(email=data_login['email']).first()
        if not usuario:
            current_app.logger.warning(f"Intento de login con email inexistente: {data_login['email']}")
            return({"message":f"Credenciales Invalidas"}), HTTPStatus.UNAUTHORIZED
          
        if not check_password_hash(usuario.password_hash, data_login.get("password_hash")):        
            smorest_abort (HTTPStatus.UNAUTHORIZED, message=f"Credenciales Invalidas password")
              
        # Generar token de authentication
        additional_claims = {"rol": usuario.rol}
        access_token = create_access_token(identity=usuario.id, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=usuario.id)        
        
        response = {
          "access_token": access_token,
          "refresh_token": refresh_token,
          "usuario": {
              "id_usuario": usuario.id,
              "nombre": usuario.username,
              "email": usuario.email               
          },
          "message": "Login exitoso"
        }          

        # envio de correo 
        # send_simple_email_message(
        #       to_email=usuario.email,
        #       subject='Inicio de sesion en la API Contactos',
        #       template_name= 'login'
        #   ) 

        return response, HTTPStatus.OK

      except HTTPException as http_exc:
        raise http_exc 
      
      except Exception as e:
        current_app.logger.error(f"Error en login: {str(e)}")
        return {"success": False,
                "message": f"Error interno: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
        
        
# ------------------ Endpoint para Logout -----------------------#

@usuario_bp.route('/auth/logout')
class LogoutResource(MethodView):
  @jwt_required()
  @usuario_bp.response(HTTPStatus.OK, LogoutResponseSchema)
  @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=UserErrorSchema, description="No esta autorizado", example={"success": False, "message": "No esta autorizado"})
  @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error al generar token", example={"success": False, "message": "Error interno del servidor"})
  def post(self):
        """ Logout usuarios  """
        # jti =get_jwt()['jti']
        # db.session.add(TokenBlocklist(jti=jti))
        # db.session.commit()
        # return {"mensaje": "Sesion cerrada con exito"}        


# ------------------ Endpoint para renovar los tokens -------------------#

@usuario_bp.route('/auth/refresh')
class RefreshToken(MethodView):
  # @jwt_required()
  @usuario_bp.response(HTTPStatus.OK, TokenRefreshResponseSchema)
  @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=UserErrorSchema, description="No esta autorizado", example={"success": False, "message": "No esta autorizado"})
  @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error al generar token", example={"success": False, "message": "Error interno del servidor"})
  def post(self):
        """ Renovar los tokens """
        jwt_payload = get_jwt()
        jti = jwt_payload['jti']
        identity = get_jwt_identity()

        # # verificar si el token está revocado
        # if TokenBlocklist.query.filter_by(jti=jti).first():
        #     abort(HTTPStatus.UNAUTHORIZED, message="Refresh token revocado")

        # # Revocar el token actual
        # db.session.add(TokenBlocklist(jti=jti))
        # db.session.commit()

        # Generar nuevos tokens
        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_refresh_token(identity=identity)

        return {
            "acces_token": new_access_token,
            "refresh_token": new_refresh_token
        }
        
   
   
@usuario_bp.route('/usuario/<id_usuario>')
class UsuarioUpdateResource(MethodView):
  @usuario_bp.arguments(UserUpdateSchema)
  @usuario_bp.response(HTTPStatus.OK, UserUpdateSchema) 
  @usuario_bp.alt_response(HTTPStatus.NOT_FOUND, schema=UserErrorSchema, description="No existe un usuario con este id", example={"success": False, "message": "Not Found"})
  @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=UserErrorSchema, description="No autorizado", example={"success": False, "message": "No autorizado"})
  @usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=UserErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def put(self, update_data, id):
    """ Actualizar datos de un usuario """
    usuario = db.session.get(Usuario, id)

    if not usuario:
      smorest_abort(HTTPStatus.NOT_FOUND, message="No existe un usuario con este id")                                      
    
    try:
      # actualizar los datos del usuario
      if update_data.get("user_name"):
        usuario.user_name = update_data["user_name"]
      if update_data.get("email"):
          usuario.email = update_data["email"]           
      
      db.session.commit()
      return usuario
    except ValidationError as err:
          db.session.rollback()
          smorest_abort (HTTPStatus.INTERNAL_SERVER_ERROR, message="Error al actualizar el usuario")                     





