from marshmallow import fields, validate, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.modelos.contacts import Contacto
from src.extensions import db


class ContactoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contacto
        load_instance = True
        schema_name="ContactoSchema"
                              
    id             = fields.UUID(dump_only=True)  
    nombre         = auto_field(required=True, validate=validate.Length(min=1))
    email          = auto_field(required=True, validate=validate.Email(error="Email Invalido"))
    telefono       = auto_field(validate=validate.Length(min=7, max=20))
    fecha_creacion = fields.Date(dump_only=True)
    
    
    
# ------------------------  Schema para registrar un contacto ---------------------------------#
class ContactoRegisterSchema(Schema):

    nombre = fields.String(required=True, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=True)
    telefono = fields.String(validate=validate.Length(max=15), allow_none=True)
    
    
    
#------------------------- Schema para respuesta al registrar usuario --------------------------#
class ContactoResponseSchema(Schema):
    id_contacto = fields.String()
    nombre = fields.String()
    email = fields.Email()     
    telefono = fields.String()   
    fecha_creacion = fields.DateTime()
    
    
    
class ContactoUpdateSchema(Schema):
    class Meta:
        model = Contacto
        load_instance = True
        sqla_session = db.session
        partial = True
        schema_name= "ContactoUpdateSchema"

    nombre    = fields.Str(required=False)
    email = fields.Str(required=False)
    telefono = fields.Str(required=False)    
    
        
    
    
# ---- schema para errores de contactos ----#
class ContactoErrorSchema(Schema):
    success = fields.Boolean(load_default=False)
    message = fields.Str(required=True)

    class Meta:
        schema_name = "ContactoErrorSchema"    

