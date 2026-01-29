# Task Manager API - Robust Backend with FastAPI

Este proyecto es una API REST profesional diseñada para la gestión de tareas, con un enfoque en seguridad y arquitectura limpia. Implementa autenticación robusta y una estructura de base de datos avanzada en PostgreSQL con soporte para múltiples esquemas.

## 🚀 Key Features

* **JWT Authentication:** Sistema de login seguro utilizando tokens de acceso (JSON Web Tokens).
* **Password Security:** Hashing mediante `bcrypt` para asegurar que las credenciales nunca se almacenen en texto plano.
* **Clean Architecture:** Separación estricta de responsabilidades en módulos (`models`, `schemas`, `crud`, `auth`).
* **Advanced PostgreSQL:** Organizado a través de **Schemas** independientes para usuarios y tareas.
* **Infrastructure as Code:** Configuración completa con **Docker** para despliegues consistentes en cualquier entorno.
* **Integrity Validation:** Restricciones de base de datos (`CHECK constraints`) para estados de tareas como `pending` y `completed`.

## 🛠 Tech Stack

* **Language:** Python 3.9+
* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Database:** PostgreSQL
* **DevOps:** Docker & Docker Compose

## 📁 Project Structure

```text
├── app/
│   ├── main.py          # Punto de entrada y definición de Endpoints
│   ├── auth.py          # Lógica de seguridad, hashing y JWT
│   ├── crud.py          # Operaciones de base de datos (Create, Read, Update, Delete)
│   ├── models.py        # Modelos de tablas SQLAlchemy
│   └── schemas.py       # Modelos de validación de datos Pydantic
├── database.py        # Configuración y conexión a PostgreSQL
├── Dockerfile         # Configuración de imagen de contenedor
├── .dockerignore      # Archivos excluidos del build de Docker
├── requirements.txt   # Lista de dependencias del proyecto
└── tasks_bd.sql       # Script SQL para la creación de la estructura de DB