from marshmallow import fields, validate, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.extensions import db
from src.modelos.pais_model import Pais


class PaisSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pais
        load_instance = True
        schema_name="PaisSchema"
                              
    pais_id      = fields.UUID(dump_only=True)  
    nombre_pais  = auto_field(required=True, validate=validate.Length(min=1))
    fecha_registro = fields.Date(dump_only=True)
    
    
    
# # ------------------------  Schema para registrar un pais ---------------------------------#
class PaisRegisterSchema(Schema):

    nombre_pais = fields.String(required=True, validate=validate.Length(min=1, max=60))    
    codigo_iso  = fields.String(required=True, validate=validate.Length(min=2))
    
    
    
# #------------------------- Schema para respuesta al registrar un pais --------------------------#
class PaisResponseSchema(Schema):
    
    pais_id = fields.String()
    nombre_pais = fields.String()
    fecha_registro = fields.Date(dump_only=True)    
    
    
    
class PaisUpdateSchema(Schema):
    
    class Meta:
        model = Pais
        load_instance = True
        sqla_session = db.session
        partial = True
        schema_name= "PaisUpdateSchema"

    nombre_pais = fields.Str(required=False)    
    codigo_iso = fields.Str(required=False)
    
        
    
    
# ---- schema para errores de pais ----#
class PaisErrorSchema(Schema):
    success = fields.Boolean(load_default=False)
    message = fields.Str(required=True)

    class Meta:
        schema_name = "PaisErrorSchema"    

