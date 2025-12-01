from flask_smorest import Blueprint, abort as smorest_abort
from flask import jsonify, current_app
from src.extensions import db
from src.modelos.pais_model import Pais
from src.schemas.pais_schema import PaisSchema, PaisRegisterSchema, PaisResponseSchema, PaisUpdateSchema, PaisErrorSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required
from flask.views import MethodView 
import uuid
from datetime import timezone, datetime
from http import HTTPStatus
from werkzeug.exceptions import HTTPException
import traceback


 
pais_bp = Blueprint('Pais', __name__, description='Operaciones con pais')


@pais_bp.route('/paises')
class CategoriaResource(MethodView):
  @pais_bp.response(HTTPStatus.OK, PaisSchema(many=True))
  @pais_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=PaisErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @pais_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=PaisErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self):
      """
      Listar todas los paises.      
      """    
      list_paises = Pais.query.all()    
      
      return list_paises, HTTPStatus.OK
      
      


@pais_bp.route('/pais/<string:pais_id>')
class UserResourceId(MethodView):
  @pais_bp.response(HTTPStatus.OK, PaisSchema)
  @pais_bp.alt_response(HTTPStatus.NOT_FOUND, schema=PaisErrorSchema, description="pais no encontrada", example={"succes": False, "message": "pais no encontrado"})
  @pais_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=PaisErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @pais_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=PaisErrorSchema, description="Error interno del servidor", example={"succes": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def get(self, pais_id):
      """
      Obtener una pais por su id.      
      """    
      
      pais = Pais.query.filter_by(pais_id=pais_id).first()
      if not pais:
        smorest_abort(HTTPStatus.NOT_FOUND, description="pais no encontrado")
            
      return pais, HTTPStatus.OK   




@pais_bp.route('/pais/register')
class PaisRegisterResource(MethodView):  
  @pais_bp.arguments(PaisRegisterSchema)
  @pais_bp.response(HTTPStatus.CREATED, PaisResponseSchema)
  @pais_bp.alt_response(HTTPStatus.CONFLICT, schema=PaisErrorSchema, description="Ya existe un pais con ese nombre", example={"success": False, "message": "Ya existe un pais con ese nombre"})
  @pais_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=PaisErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def post(self, pais_data):
      """
      Registrar nuevo pais en la base de datos.
      """
      try:
          if Pais.query.filter_by(nombre_pais=pais_data['nombre_pais']).first():
            smorest_abort(HTTPStatus.CONFLICT, message=f"Ya existe un pais con ese nombre")
                
           # Crear el nuevo usuario
            new_country = Categoria(
                pais_id=str(uuid.uuid4()),
                nombre_pais=pais_data['nombre_pais'],                
                iso=codigo_iso['codigo_iso'],
                fecha_creacion=datetime.now(timezone.utc)      
            )          

          db.session.add(new_country)
          db.session.commit()

          return new_country, HTTPStatus.CREATED
       
      except HTTPException as http_exc:
        raise http_exc
      except Exception as e:
       current_app.logger.error(f"Error al registrar categoria: {str(e)}\n{traceback.format_exc()}")
       db.session.rollback()
       smorest_abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Error interno del servidor: {str(e)}")
      except ValidationError as e:
          return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST
    



@pais_bp.route('/pais/update/<string:pais_id>')  
class PaisUpdateResource(MethodView):
  @pais_bp.arguments(PaisUpdateSchema)
  @pais_bp.response(HTTPStatus.OK, PaisSchema)
  @pais_bp.alt_response(HTTPStatus.NOT_FOUND, schema=PaisErrorSchema, description="pais no encontrado", example={"succes": False, "message": "pais no encontrada"})
  @pais_bp.alt_response(HTTPStatus.CONFLICT, schema=PaisErrorSchema, description="Ya existe un pais con ese nombre", example={"success": False, "message": "Ya existe un pais con ese nombre"})
  @pais_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=PaisErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @pais_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=PaisErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  #@jwt_required() 
  def put(update_data):
    """
      Actualizar un pais existente         
    """    
    pais = db.session.get(Pais, update_data["pais_id"])
    if not pais:
        smorest_abort(HTTPStatus.NOT_FOUND, description="pais no encontrado")

    try:
        
        if update_data.get("nombre_pais"):
           if update_data["nombre_pais"] == pais.nombre_pais:
               smorest_abort(HTTPStatus.CONFLICT, message=f"Ya existe un pais con ese nombre")
           pais.nombre_pais = update_data["nombre_pais"]
        if update_data.get("codigo_iso"):
            pais.codigo_iso = update_data["codigo_iso"]  
            

        db.session.commit()      
        return pais, HTTPStatus.OK

    except ValidationError as e:
        return jsonify({"Error": e.messages}), HTTPStatus.BAD_REQUEST
    except Exception as err:
        return jsonify({"Error": str(err)}), HTTPStatus.BAD_REQUEST
    




@pais_bp.route('/pais/delete/<string:pais_id>')
class ContactoDeleteResource(MethodView):
  @pais_bp.arguments(PaisUpdateSchema)
  @pais_bp.response(HTTPStatus.OK, PaisResponseSchema)
  @pais_bp.alt_response(HTTPStatus.NOT_FOUND, schema=PaisErrorSchema, description="pais no encontrado", example={"success": False, "message": "No existe un pais con el Id proveeido"})
  @pais_bp.alt_response(HTTPStatus.CONFLICT, schema=PaisErrorSchema, description="Ya existe un pais con ese nombre", example={"success": False, "message": "Ya existe un pais con ese nombre"})
  @pais_bp.alt_response(HTTPStatus.UNAUTHORIZED, schema=PaisErrorSchema, description="No autorizado", example={"succes": False, "message": "No autorizado"})
  @pais_bp.alt_response(HTTPStatus.INTERNAL_SERVER_ERROR, schema=PaisErrorSchema, description="Error interno del servidor", example={"success": False, "message": "Error interno del servidor"})
  #@jwt_required()
  def delete(delete_data):
      """
      Eliminar un pais existente    
      """    
      pais = db.session.get(Pais, delete_data["pais_id"])
      if not pais:
          smorest_abort(HTTPStatus.NOT_FOUND, description="pais no encontrado")

      db.session.delete(pais)
      db.session.commit()
      return jsonify({"mensaje": f"Registro '{pais.nombre_pais}' eliminado exitosamente"}), HTTPStatus.OK    