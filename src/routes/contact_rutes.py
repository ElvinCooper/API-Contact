from flask_smorest import Blueprint, abort as smorest_abort
from flask import jsonify, current_app, Response
from src.extensions import db
from src.modelos.contacts import Contacto
from src.modelos.users import Usuario
from src.schemas.contact_schema import ContactoSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt, get_jwt_identity
from flask.views import MethodView 
import uuid
from datetime import timezone, datetime
from http import HTTPStatus
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import HTTPException
import traceback


 
contacto_bp = Blueprint('contactos', __name__, description='Operaciones con usuarios')


@contacto_bp.route('/usuarios')
class UsuarioRegister(MethodView):
  #@usuario_bp.response(HTTPStatus.OK, UserSimpleSchema(many=True))
  # @usuario_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  #@usuario_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self):
      """
      Listar todos los contactos

      En este endpoint un usuario autenticado puede listar todos
      los contactos existentes en la base de datos.
      """    
      list_contacts = Contacto.query.all()    
      
      return list_contacts
      
      return jsonify(contacts_schema.dump(list_contacts))



# Endpoint para consultar un contacto con su id
@contacto_bp.route('/usuario/<string:id_usuario>')
class UserResourceId(MethodView):
    #@usuario_bp.response(HTTPStatus.OK, UserSimpleSchema)
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
@contacto_bp.route('/auth/register')
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
    


# Endpoint para actualizar un recurso en la bd
# @contacto_bp.route('/contactos/<string:id>', methods=['PUT'])  
# @jwt_required() 
# def update_contact(id):
#     """
#     Actualizar un contacto existente

#     Este endpoint permite al usuario autenticado actulizar la informacion
#     de un contacto ya se manera parcial o completa indicando su id.
    
#     """    
#     contacto = db.session.get(Contacto, id)
#     if not contacto:
#         abort(404, description="Contacto no encontrado")

#     try:
#         json_data = request.get_json()
#         if not json_data:
#             return jsonify({"mensaje": "No hay datos proveidos"}), 400
#         data = contacto_schema.load(json_data, session=db.session, partial=True)        
         
#         contacto.nombre   = data.nombre   or contacto.nombre
#         contacto.email    = data.email    or contacto.email
#         contacto.telefono = data.telefono or contacto.telefono

#         db.session.commit()
        
#         return jsonify(contacto_schema.dump(contacto))               
#     except ValidationError as e:
#         return jsonify({"Error": e.messages}), 400
#     except Exception as err:
#         return jsonify({"Error": str(err)}), 400    
    



# ENDPOINT PARA ELIMINAR UN RECURSO DE LA BD
# @contacto_bp.route('/contactos/<string:id>', methods=['DELETE'])
# @jwt_required()
# def delete_contact(id):
#     """
#     Eliminar un contacto

#     Este endpoint permite al usuario autenticado eliminar 
#     a un contacto indicando su id.
#     ---
#     tags:
#       - Contactos
#     security:
#       - BearerAuth: []
#     parameters:
#       - name: id
#         in: path
#         type: string
#         required: true
#         description: ID del contacto a eliminar
#     responses:
#       200:
#         description: Contacto eliminado exitosamente
#       404:
#         description: Contacto no encontrado
#     """    
#     contacto = db.session.get(Contacto, id)
#     if not contacto :
#         abort(400, description="Contacto no encontrado")

#     db.session.delete(contacto)
#     db.session.commit()
#     return jsonify({"mensaje": f"Registro '{contacto.nombre}' eliminado exitosamente"}), 200    