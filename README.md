# 📇 API de Contactos con Flask

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-green?logo=flask)
![License](https://img.shields.io/github/license/ElvinCooper/-Contact_api)

Una API RESTful para la gestión de contactos, desarrollada con **Flask**, **JWT**, **SQLAlchemy**, **Swagger**, **Marshmallow** y más.

---

## 🧭 Tabla de Contenido

- [🚀 Funcionalidades](#-funcionalidades)
- [🛠️ Instalación](#️-instalación)
- [🔐 Rutas protegidas](#-rutas-protegidas)
- [📚 Documentación Swagger](#-documentación-swagger)
- [🧪 Pruebas con Pytest](#-pruebas-con-pytest)
- [🗂 Estructura del proyecto](#-estructura-del-proyecto)
- [📦 Requisitos](#-requisitos)
- [🤝 Contribuciones](#-contribuciones)

---

## 🚀 Funcionalidades

- 🧾 Registro y login de usuarios con **JWT**
- 📇 CRUD completo para contactos
- 🔐 Rutas protegidas mediante autenticación
- 📚 Documentación interactiva con **Swagger**
- 📨 Envío de correos al registrarse o iniciar sesión (opcional con Mailgun)
- 🧪 Pruebas automatizadas con **Pytest**
- 📁 Estructura modular con **Blueprints** y validación con **Marshmallow**

---

## 🛠️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/ElvinCooper/-Contact_api.git
cd -Contact_api
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/macOS
source venv/bin/activate

### 2. Crea un entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Crea el archivo `.env`

```env
JWT_SECRET_KEY=tu_clave_secreta_para_jwt
SECRET_KEY=tu_clave_general
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///mis_contactos.db
MAILGUN_API_KEY=tu_api_key_mailgun
MAILGUN_DOMAIN=sandboxXXXX.mailgun.org
MAILGUN_FROM=Mailgun Sandbox <postmaster@sandboxXXXX.mailgun.org>
FRONTEND_URL= 
```

> ⚠️ Si no usarás correos, puedes dejar los campos vacíos temporalmente.

---

## 🗃️ Base de datos

### Iniciar migraciones

```bash
flask db init
flask db migrate -m "init"
flask db upgrade
```

### Crear la base de datos (opcional para desarrollo o testing):

```bash
flask db_create
```

---

## ▶️ Ejecutar el servidor

```bash
flask run --debug  # Esto activa el servidor en modo debuging para desarrllo 
```

---

## 🔐 Rutas protegidas con JWT

Para acceder a las rutas privadas:

1. Regístrate en `/api/register`
2. Haz login en `/api/login` y copia el token
3. En Swagger UI haz clic en `Authorize` y pega:

```
Bearer (espacio) + (tu token)  
```

---

## 📚 Documentación Swagger

Accede a la documentación interactiva en:

```
https://contact-api-8rpp.onrender.com/apidocs
```

Desde ahí puedes probar todos los endpoints directamente.

---

## 🧪 Pruebas con Pytest

```bash
pytest -v
```

> Las pruebas usan una base de datos en memoria (`sqlite:///:memory:`).

---

## 🗂 Estructura del proyecto

```
/contact_api/
├── app.py
├── config.py
├── extensions.py
├── /modelos/
├── /routes/
├── /schemas/
├── /templates/
├── /tests/
├── migrations/
├── .env
└── requirements.txt
```

---

▶️ Ejecutar el servidor

# En modo desarrollo
flask run --debug

# O ejecutando directamente app.py
python app.py


---

## 📦 Requisitos

- Python 3.11+
- pip
- SQLite (o configurar tu propio motor SQL)

---

## 🧑‍💻 Contribuciones

¡Toda contribución es bienvenida!  
Puedes abrir issues o pull requests si deseas proponer mejoras, reportar bugs o aportar con nuevas funciones.

---

## 📜 Licencia

MIT License
```
