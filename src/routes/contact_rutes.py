from flask import Blueprint, request, jsonify, abort, Response
from src.extensions import db
from src.modelos.contacts import Contacto
from src.schemas.contact_schema import ContactoSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required

 
contacto_bp = Blueprint('contactos', __name__)
contacto_schema = ContactoSchema()
contacts_schema = ContactoSchema(many=True)



# Enpoint de Bienvenida 
@contacto_bp.route('/')
def index():
    """
    Bienvenida a la API de Contactos
    ---
    tags:
      - Contactos
    responses:
      200:
        description: Mensaje de bienvenida
    """    
    return jsonify({"message": "API de Contactos activa"}), 200



# Enpoint para consultar todos los datos de la tabla de contactos
@contacto_bp.route('/contactos', methods=['GET', 'OPTIONS'])
@jwt_required()
def listar_contactos():
    """
    Listar todos los contactos

    En este endpoint un usuario autenticado puede listar todos
    los contactos existentes en la base de datos.
    ---
    tags:
      - Contactos
    security:
      - BearerAuth: []
    responses:
      200:
        description: Lista de contactos
    """    
    if request.method == 'OPTIONS':
          # Responder a solicitudes preflight de CORS
          response = Response(status=200)
          response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
          response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
          response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
          return response

    list_contacts = Contacto.query.all()    
    
    return jsonify(contacts_schema.dump(list_contacts))



# Endpoint para consultar un contacto con su id
@contacto_bp.route('/contactos/<string:id>' , methods=['GET'])
@jwt_required()
def get_contactos(id):
    """
    Obtener contacto por ID

    Este endpoint permite al usuario obtener los datos de un contacto 
    por su respectivo ID
    ---
    tags:
      - Contactos
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del contacto
    responses:
      200:
        description: Contacto encontrado
      404:
        description: Contacto no encontrado
    """    
    contacto = db.session.get(Contacto, id)
    if not contacto:
      abort(404, description="Contacto no encontrado")
           
    return jsonify(contacto_schema.dump(contacto)), 200    



# Enpoint para insertar un contacto
@contacto_bp.route('/contactos', methods=['POST'])
@jwt_required()
def create_contact():
    """
    Crear nuevo contacto en la base de datos.

    Este endpoint permite a un usuario autenticado crear un nuevo contacto
    proporcionando nombre, email y teléfono.
    ---
    tags:
      - Contactos
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: contacto
        required: true
        schema:
          id: NuevoContacto
          required:
            - nombre
            - email
            - telefono
          properties:
            nombre:
              type: string
              example: Ana Pérez
            email:
              type: string
              example: ana@example.com
            telefono:
              type: string
              example: "123456789"
    responses:
      201:
        description: Contacto creado exitosamente
      400:
        description: Datos inválidos o email duplicado
    """
    try:
        json_data = request.get_json()
        nombre = json_data.get('nombre')
        email = json_data.get('email')
        telefono = json_data.get('telefono')

        data = contacto_schema.load(json_data, session=db.session)

        # verificar si ya existe un usuario con el mismo email
        if Contacto.query.filter_by(email=data.email).first():        
           return jsonify({"mensaje": "Ya existe un contacto con este email"}), 400


        nuevo_contacto = Contacto(
            nombre= nombre,
            email = email,
            telefono = telefono            
            )
        db.session.add(nuevo_contacto)
        db.session.commit()

        return jsonify(contacto_schema.dump(nuevo_contacto)), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    


# Endpoint para actualizar un recurso en la bd
@contacto_bp.route('/contactos/<string:id>', methods=['PUT'])  
@jwt_required() 
def update_contact(id):
    """
    Actualizar un contacto existente

    Este endpoint permite al usuario autenticado actulizar la informacion
    de un contacto ya se manera parcial o completa indicando su id.
    ---
    tags:
      - Contactos
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del contacto a actualizar
      - in: body
        name: contacto
        schema:
          id: ContactoUpdate
          properties:
            nombre:
              type: string
              example: Ana Pérez
            email:
              type: string
              example: nuevo@example.com
            telefono:
              example: "826542365"  
    responses:
      200:
        description: Contacto actualizado
      400:
        description: Error en los datos o excepción inesperada
      404:
        description: Contacto no encontrado
    """    
    contacto = db.session.get(Contacto, id)
    if not contacto:
        abort(404, description="Contacto no encontrado")

    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"mensaje": "No hay datos proveidos"}), 400
        data = contacto_schema.load(json_data, session=db.session, partial=True)        
         
        contacto.nombre   = data.nombre   or contacto.nombre
        contacto.email    = data.email    or contacto.email
        contacto.telefono = data.telefono or contacto.telefono

        db.session.commit()
        
        return jsonify(contacto_schema.dump(contacto))               
    except ValidationError as e:
        return jsonify({"Error": e.messages}), 400
    except Exception as err:
        return jsonify({"Error": str(err)}), 400    
    



# ENDPOINT PARA ELIMINAR UN RECURSO DE LA BD
@contacto_bp.route('/contactos/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_contact(id):
    """
    Eliminar un contacto

    Este endpoint permite al usuario autenticado eliminar 
    a un contacto indicando su id.
    ---
    tags:
      - Contactos
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID del contacto a eliminar
    responses:
      200:
        description: Contacto eliminado exitosamente
      404:
        description: Contacto no encontrado
    """    
    contacto = db.session.get(Contacto, id)
    if not contacto :
        abort(400, description="Contacto no encontrado")

    db.session.delete(contacto)
    db.session.commit()
    return jsonify({"mensaje": f"Registro '{contacto.nombre}' eliminado exitosamente"}), 200    