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
    
    
# ------------------------  Schema para registrar un usuario ---------------------------------#
class UserRegisterSchema(Schema):

    user_name = fields.String(required=True, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=25), load_only=True)    
    
    
#------------------------- Schema para respuesta al registrar usuario --------------------------#
class UserResponseSchema(Schema):
    id = fields.String()
    user_name = fields.String()
    email = fields.Email()    
    
    
# --------------------- Schema para la respuesta del Logout ---------------------------------------#
class LogoutResponseSchema(Schema):
    class Meta:
        model = Usuario
        load_instance = True
        include_relationships = False  # No incluir relaciones en actualización
        sqla_session = db.session
        partial = True  # Para actualizaciones parciales
        schema_name = "UserLogoutSchema"

    mensaje = fields.String()    
    
    
# --------------------- Schema para la respuesta del refresh token ---------------------------------------#
class TokenRefreshResponseSchema(Schema):
    class Meta:
            model = Usuario
            load_instance = True
            include_relationships = False  # No incluir relaciones en actualización
            sqla_session = db.session
            partial = True  # Para actualizaciones parciales
            schema_name = "TokenRefreshSchema"

    acces_token = fields.String(required=True)
    refresh_token = fields.String(required=True)    
    
    
    
# ------------------------  Schema para actualizacion ---------------------------------#    
class UserUpdateSchema(Schema):
    class Meta:
        model = Usuario
        load_instance = True
        # include_relationships = False  
        sqla_session = db.session
        partial = True 
        schema_name = "UserUpdateSchema"
        # fields = ("user_name", "email")
    
    # Campos que se pueden actualizar
    user_name = fields.Str(required=False, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=False)
    
    

# ---- schema para errores de users----#
class UserErrorSchema(Schema):
    success = fields.Boolean(load_default=False)
    message = fields.Str(required=True)

    class Meta:
        schema_name = "UserErrorSchema"
        