# 📇 API de Contactos con Flask

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-green?logo=flask)
[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
[![Pytest](https://img.shields.io/badge/Pytest-fff?logo=pytest&logoColor=000)](#)
[![CI Pipeline](https://github.com/ElvinCooper/API-Contact/actions/workflows/test_and_deploy.yml/badge.svg?branch=main)](https://github.com/ElvinCooper/API-Contact/actions/workflows/test_and_deploy.yml)

[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=173647)](#)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-6BA539?logo=openapiinitiative&logoColor=white)](#)
[![PyCharm](https://img.shields.io/badge/PyCharm-000?logo=pycharm&logoColor=fff)](https://www.jetbrains.com/pycharm/)

[![LinkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff)](https://www.linkedin.com/in/elvin-cooper-8a5647b6/)


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
- 🐳 Contenerización y Despliegue Fácil con Dockerfile y Docker-compose.yaml para entornos de desarrollo instantáneo como Codespaces.

---

## 🛠️ Instalación

1. Clonar el repositorio
git clone https://github.com/ElvinCooper/API-Contact.git
cd API-Contact
2. Crea el archivo .env Este archivo es crucial para la configuración de secretos y la base de datos.
JWT_SECRET_KEY = tu_clave_secreta_para_jwt
SECRET_KEY = tu_clave_general
FLASK_ENV = development
SQLALCHEMY_DATABASE_URI = sqlite:///mis_contactos.db
MAILGUN_API_KEY = tu_api_key_mailgun
MAILGUN_DOMAIN = sandboxXXXX.mailgun.org
MAILGUN_FROM = Mailgun Sandbox <postmaster@sandboxXXXX.mailgun.org>
FRONTEND_URL =
⚠️ Si no usarás correos, puedes dejar los campos vacíos temporalmente.

--------------------------------------------------------------------------------
Opción 1: Despliegue con Docker y Codespaces (Recomendado)
Utilice esta opción si tiene Docker instalado o si está usando Codespaces, ya que proporciona un entorno de desarrollo consistente, listo para usar, tal como se implementa en Inventario-Docker.
1. Requisitos Previos: Docker y Docker Compose (o usar Codespaces).
2. Levantar los servicios:
3. Verificación: Acceda a la documentación Swagger en la ruta local (http://localhost:5000/apidocs o el puerto configurado).
Opción 2: Desarrollo Local (Sin Docker)
Use esta opción si prefiere configurar el entorno Python manualmente.
1. Crea un entorno virtual:
2. Instala las dependencias:
3. Base de datos y Migraciones: Inicie las migraciones de la base de datos:
4. Ejecutar el servidor:
5. Esto activará el servidor en modo debugging para desarrollo.
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
/API-Contact/
├── .devcontainer/        # Archivos de configuración para Codespaces/Contenedor de Desarrollo
├── src/                  # DIRECTORIO PRINCIPAL de la lógica de la aplicación
│   ├── modelos/          # Modelos SQLAlchemy (Contacto, Usuario, Categoria, Pais)
│   ├── routes/           # Blueprints y rutas
│   ├── schemas/          # Esquemas de Marshmallow
│   ├── extensions.py
│   └── ...
├── migrations/           # Migraciones de base de datos (Alembic)
├── templates/ emails/    # Plantillas de correo [2]
├── tests/                # Pruebas automatizadas con Pytest [2]
├── Docker-compose.yaml   # Configuración de Docker Compose (API + DB si aplica)
├── Dockerfile            # Imagen de la aplicación Flask
├── requirements.txt
├── requirements-dev.txt  # Nuevas dependencias de desarrollo
└── README.md
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




