from flask_smorest import Blueprint, abort as smorest_abort
from flask import jsonify, current_app
from src.extensions import db
from src.modelos.category_model import Categoria
from src.schemas.category_schema import Categoria, CategoriaErrorSchema, CategoriaRegisterSchema, CategoriaResponseSchema, CategoriaUpdateSchema, CategoriaSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView 
import uuid
from datetime import timezone, datetime
from http import HTTPStatus
from werkzeug.exceptions import HTTPException
import traceback


 
categoria_bp = Blueprint('Categorias', __name__, description='Operaciones con categorias')


@categoria_bp.route('/categorias')
class CategoriaResource(MethodView):
  @categoria_bp.response(HTTPStatus.OK, CategoriaSchema(many=True))
  @categoria_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=CategoriaErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @categoria_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=CategoriaErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self):
      """
      Listar todas las categorias      
      """    
      list_categories = Categoria.query.all()    
      
      return list_categories, HTTPStatus.OK
      
      

# Endpoint para consultar un contacto con su id
@categoria_bp.route('/categoria/<string:id_categoria>')
class UserResourceId(MethodView):
  @categoria_bp.response(HTTPStatus.OK, CategoriaSchema)
  @categoria_bp.alt_response(HTTPStatus.NOT_FOUND, schema=CategoriaErrorSchema, description="Categoria no encontrada", example={"succes": False, "message": "Categoria no encontrada"})
  @categoria_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=CategoriaErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @categoria_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=CategoriaErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self, id_categoria):
      """
      Obtener una categoria por su id.      
      """    
      
      categoria = Categoria.query.filter_by(id_categoria=id_categoria).first()
      if not categoria:
        smorest_abort(HTTPStatus.NOT_FOUND, description="Categoria no encontrada")
            
      return categoria, HTTPStatus.OK   




@categoria_bp.route('/categoria/register')
class ContactoRegisterResource(MethodView):  
  @categoria_bp.arguments(CategoriaRegisterSchema)
  @categoria_bp.response(HTTPStatus.CREATED, CategoriaResponseSchema)
  @categoria_bp.alt_response(HTTPStatus.CONFLICT, schema=CategoriaErrorSchema, description="Ya existe una categoria con ese nombre", example={"success": False, "message": "Ya existe una categoria con ese nombre"})
  @categoria_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=CategoriaErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  @jwt_required()
  def post(self, categoria_data):
      """
      Registrar nueva categoria en la base de datos.
      """
      try:
          if Categoria.query.filter_by(nombre_categoria=categoria_data['nombre_categoria']).first():
               smorest_abort(HTTPStatus.CONFLICT, message=f"Ya existe un categoria con ese nombre")
                
          # Crear el nuevo usuario
          new_category = Categoria(
            id_categoria=str(uuid.uuid4()),
            nombre_categoria=categoria_data['nombre_categoria'],
            fecha_creacion=datetime.now(timezone.utc) )

          db.session.add(new_category)
          db.session.commit()

          return new_category, HTTPStatus.CREATED
       
      except HTTPException as http_exc:
        raise http_exc
      except Exception as e:
       current_app.logger.error(f"Error al registrar categoria: {str(e)}\n{traceback.format_exc()}")
       db.session.rollback()
       smorest_abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(e)}")
      except ValidationError as e:
          return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
    



# Endpoint para actualizar un contacto en la bd
@categoria_bp.route('/categoria/update/<string:id_categoria>')  
class ContactoUpdateResource(MethodView):
  @categoria_bp.arguments(CategoriaUpdateSchema)
  @categoria_bp.response(HTTPStatus.OK, CategoriaSchema)
  @categoria_bp.alt_response(HTTPStatus.NOT_FOUND, schema=CategoriaErrorSchema, description="Categoria no encontrada", example={"succes": False, "message": "Categoria no encontrada"})
  @categoria_bp.alt_response(HTTPStatus.CONFLICT, schema=CategoriaErrorSchema, description="Ya existe una categoria con ese nombre", example={"success": False, "message": "Ya existe una categoria con ese nombre"})
  @categoria_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=CategoriaErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @categoria_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=CategoriaErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  #@jwt_required() 
  def put(update_data):
      """
      Actualizar una categoria existente     
    
      """    
      categoria = db.session.get(Categoria, update_data["id_categoria"])
      if not categoria:
        smorest_abort(HTTPStatus.NOT_FOUND, description="Categoria no encontrado")

      try:
          
        if update_data.get("nombre_categoria"):
           if update_data["nombre_categoria"] == categoria.nombre_categoria:
              smorest_abort(HTTPStatus.CONFLICT, message=f"Ya existe una categoria con ese nombre")
           categoria.nombre_categoria = update_data["nombre_categoria"]

        db.session.commit()      
        return categoria, HTTPStatus.OK
      
      except ValidationError as e:
          return jsonify({"Error": e.messages}), HTTPStatus.BAD_REQUEST
      except Exception as err:
          return jsonify({"Error": str(err)}), HTTPStatus.BAD_REQUEST
    




@categoria_bp.route('/categoria/delete/<string:id_categoria>')
class ContactoDeleteResource(MethodView):
  @categoria_bp.arguments(CategoriaUpdateSchema)
  @categoria_bp.response(HTTPStatus.OK, CategoriaResponseSchema)
  @categoria_bp.alt_response(HTTPStatus.NOT_FOUND, schema=CategoriaErrorSchema, description="categoria no encontrada", example={"success": False, "message": "No existe una categoria con el Id proveeido"})
  @categoria_bp.alt_response(HTTPStatus.CONFLICT, schema=CategoriaErrorSchema, description="Ya existe una categoria con ese nombre", example={"success": False, "message": "Ya existe un categoria con ese nombre"})
  @categoria_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=CategoriaErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @categoria_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=CategoriaErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def delete(delete_data):
      """
      Eliminar una categoria existente    
      """    
      categoria = db.session.get(Categoria, delete_data["id_categoria"])
      if not categoria:
          smorest_abort(HTTPStatus.NOT_FOUND, description="categoria no encontrada")

      db.session.delete(categoria)
      db.session.commit()
      return jsonify({"mensaje": f"Registro '{categoria.nombre_categoria}' eliminado exitosamente"}), HTTPStatus.OK    