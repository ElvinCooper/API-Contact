from marshmallow import fields, validate, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from src.modelos.users import Usuario
from src.extensions import db


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
                        
    id       = fields.String(dump_only=True)  
    username = auto_field(required=True, validate=validate.Length(min=1, max=60))
    email    = fields.Email(required=True) 
    password = auto_field(required=True, validate=validate.Length(min=8, max=25))
    
    
    
    
class UserSimpleSchema(Schema):
    class Meta:
        model = Usuario
        load_instance = True
        sqla_session = db.session
        schema_name = "UserSimpleSchema"

    id_usuario = fields.Str(dump_only=True)
    user_name = fields.Str()
    email = fields.Email()
    