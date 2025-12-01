from marshmallow import fields, validate, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.extensions import db
from src.modelos.category_model import Categoria


class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = True
        schema_name="CategoriaSchema"
                              
    id_categoria      = fields.UUID(dump_only=True)  
    nombre_categoria  = auto_field(required=True, validate=validate.Length(min=1))
    fecha_creacion = fields.Date(dump_only=True)
    
    
    
# # ------------------------  Schema para registrar un contacto ---------------------------------#
class CategoriaRegisterSchema(Schema):

    nombre_categoria = fields.String(required=True, validate=validate.Length(min=1, max=60))    
    
    
    
# #------------------------- Schema para respuesta al registrar usuario --------------------------#
class CategoriaResponseSchema(Schema):
    
    id_categoria = fields.String()
    nombre_categoria = fields.String()
    fecha_creacion = fields.Date(dump_only=True)    
    
    
    
class CategoriaUpdateSchema(Schema):
    
    class Meta:
        model = Categoria
        load_instance = True
        sqla_session = db.session
        partial = True
        schema_name= "CategoriaUpdateSchema"

    nombre_categoria = fields.Str(required=False)    
    
        
    
    
# ---- schema para errores de contactos ----#
class CategoriaErrorSchema(Schema):
    success = fields.Boolean(load_default=False)
    message = fields.Str(required=True)

    class Meta:
        schema_name = "CategoriaErrorSchema"    

