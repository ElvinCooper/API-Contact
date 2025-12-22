from flask_smorest import Blueprint, abort as smorest_abort
from flask import jsonify, current_app
from src.extensions import db
from src.modelos.contacts import Contacto
from src.modelos.users import Usuario
from src.schemas.contact_schema import ContactoSchema, ContactoErrorSchema, ContactoRegisterSchema, ContactoResponseSchema, ContactoUpdateSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView 
import uuid
from datetime import timezone, datetime
from http import HTTPStatus
from werkzeug.exceptions import HTTPException
import traceback


 
contacto_bp = Blueprint('Contactos', __name__, description='Operaciones con contactos')


@contacto_bp.route('/contactos')
class ContactosResource(MethodView):
  @contacto_bp.response(HTTPStatus.OK, ContactoSchema(many=True))
  @contacto_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ContactoErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @contacto_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ContactoErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  @jwt_required()
  def get(self):
      """
      Listar todos los contactos

      En este endpoint un usuario autenticado puede listar todos
      los contactos existentes en la base de datos.
      """    
      list_contacts = Contacto.query.all()    
      
      return list_contacts, HTTPStatus.OK
      
      

# Endpoint para consultar un contacto con su id
@contacto_bp.route('/contacto/<string:id_contacto>')
class UserResourceId(MethodView):
  @contacto_bp.response(HTTPStatus.OK, ContactoSchema)
  @contacto_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ContactoErrorSchema, description="Usuario no encontrado", example={"succes": False, "message": "Usuario no encontrado"})
  @contacto_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ContactoErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @contacto_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ContactoErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  @jwt_required()
  def get(self, id_contacto):
      """
      Obtener contacto por ID

      Este endpoint permite al usuario obtener los datos de un contacto por su respectivo id.
      """    
      contacto = Usuario.query.filter_by(id_usuario=id_contacto).first()
      if not contacto:
        smorest_abort(HTTPStatus.NOT_FOUND, description="Contacto no encontrado")
            
      return contacto, HTTPStatus.OK    




# Enpoint para ingresar  un contacto
@contacto_bp.route('/contacto/register')
class ContactoRegisterResource(MethodView):
  #@limiter.limit("5 per minute")  # intentos por minuto
  @contacto_bp.arguments(ContactoRegisterSchema)
  @contacto_bp.response(HTTPStatus.CREATED, ContactoResponseSchema)
  @contacto_bp.alt_response(HTTPStatus.CONFLICT, schema=ContactoErrorSchema, description="Ya existe un usuario con ese email", example={"success": False, "message": "Ya existe un usuario con ese email"})
  @contacto_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ContactoErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  def post(self, contacto_data):
      """
      Registrar nuevo contacto en la base de datos.

      Este endpoint permite a un usuario autenticado crear un nuevo contacto
      proporcionando nombre, email y teléfono.
      """
      try:
          if Usuario.query.filter_by(email=contacto_data['email']).first():
            smorest_abort(HTTPStatus.CONFLICT, message=f"Ya existe un contacto con ese email")
                
          # Crear el nuevo usuario
          new_contacto = Contacto(
              id_contacto=str(uuid.uuid4()),
              nombre=contacto_data['nombre'],
              email=contacto_data['email'],
              telefono=contacto_data['telefono'],
              fecha_creacion=datetime.now(timezone.utc)
          )

          db.session.add(new_contacto)
          db.session.commit()

          return new_contacto, HTTPStatus.CREATED
       
      except HTTPException as http_exc:
        raise http_exc
      except Exception as e:
       current_app.logger.error(f"Error al registrar contacto: {str(e)}\n{traceback.format_exc()}")
       db.session.rollback()
       smorest_abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(e)}")
      except ValidationError as e:
          return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
    


# Endpoint para actualizar un contacto en la bd
@contacto_bp.route('/contacto/update/<string:id_contacto>')  
class ContactoUpdateResource(MethodView):
  @contacto_bp.arguments(ContactoUpdateSchema)
  @contacto_bp.response(HTTPStatus.CREATED, ContactoResponseSchema)
  @contacto_bp.alt_response(HTTPStatus.CONFLICT, schema=ContactoErrorSchema, description="Ya existe un contacto con ese email", example={"success": False, "message": "Ya existe un contacto con ese email"})
  @contacto_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ContactoErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @contacto_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ContactoErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  @jwt_required()
  def put(self, update_data, id_contacto):
      """
      Actualizar un contacto existente

      Este endpoint permite al usuario autenticado actulizar la informacion
      de un contacto ya se manera parcial o completa indicando su id.
    
      """    
      contacto = db.session.get(Contacto, id_contacto)
      if not contacto:
        smorest_abort(HTTPStatus.NOT_FOUND, description="Contacto no encontrado")

      try:
          
        if "nombre" in update_data:
          contacto.nombre = update_data["nombre"]
        if "email" in update_data:
          contacto.email = update_data["email"]
        if "telefono" in update_data:
          contacto.telefono = update_data["telefono"]
          contacto.telefono = update_data["telefono"]

        db.session.commit()
      
        return contacto
      except ValidationError as e:
          return jsonify({"Error": e.messages}), HTTPStatus.BAD_REQUEST
      except Exception as err:
          return jsonify({"Error": str(err)}), HTTPStatus.BAD_REQUEST
    



# ENDPOINT PARA ELIMINAR UN RECURSO DE LA BD
@contacto_bp.route('/contacto/delete/<string:id_contacto>')
class ContactoDeleteResource(MethodView):
  @contacto_bp.response(HTTPStatus.OK, ContactoResponseSchema)
  @contacto_bp.alt_response(HTTPStatus.NOT_FOUND, schema=ContactoErrorSchema, description="contacto no encontrado", example={"success": False, "message": "No existe un contacto con el Id proveeido"})
  @contacto_bp.alt_response(HTTPStatus.CONFLICT, schema=ContactoErrorSchema, description="Ya existe un contacto con ese email", example={"success": False, "message": "Ya existe un contacto con ese email"})
  @contacto_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=ContactoErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @contacto_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=ContactoErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  @jwt_required()
  def delete(self, id_contacto):
      """
      Eliminar un contacto

      Este endpoint permite al usuario autenticado eliminar 
      a un contacto indicando su id.
      """    
      contacto = db.session.get(Contacto, id_contacto)
      if not contacto :
          smorest_abort(HTTPStatus.NOT_FOUND, description="Contacto no encontrado")

      db.session.delete(contacto)
      db.session.commit()
      return jsonify({"mensaje": f"Registro '{contacto.nombre}' eliminado exitosamente"}), HTTPStatus.OK    