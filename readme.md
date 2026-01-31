# 🚀 Task Manager API - Cloud & Docker Ready

Este proyecto es una API REST profesional diseñada para la gestión de tareas, construida con **FastAPI** y **PostgreSQL**. La arquitectura está optimizada para ser desplegada en contenedores **Docker** y escalada en la nube (**AWS**), garantizando consistencia total entre los entornos de desarrollo y producción.

## 🌟 Key Features

* **JWT Authentication:** Sistema de seguridad basado en tokens (JSON Web Tokens) para acceso protegido y gestión de sesiones.
* **Password Hashing:** Implementación de `bcrypt` para asegurar el almacenamiento de credenciales.
* **Containerized Architecture:** Orquestación completa con **Docker Compose** para servicios de Backend y Base de Datos independientes.
* **Database Resilience:** Persistencia de datos mediante volúmenes de Docker y carga automática del esquema PostgreSQL mediante scripts de inicialización.
* **Cloud Optimized:** Configuración lista para despliegue inmediato en **AWS** (App Runner, ECS o EC2).
* **Clean Architecture:** Estructura modular que separa modelos de datos, validaciones (Pydantic) y lógica de negocio (CRUD).

## 🛠 Tech Stack

* **Backend:** Python 3.11+ | FastAPI | SQLAlchemy (ORM)
* **Database:** PostgreSQL 15 (Alpine)
* **DevOps:** Docker | Docker Compose | AWS
* **Security:** JWT | Passlib (Bcrypt)

## 📁 Project Structure

```text
├── backend/            # Lógica central del servidor (FastAPI)
│   ├── main.py         # Punto de entrada de la API y rutas
│   ├── auth.py         # Lógica de seguridad y JWT
│   ├── crud.py         # Operaciones de base de datos
│   ├── models.py       # Modelos de tablas SQLAlchemy
│   ├── schemas.py      # Modelos de validación Pydantic
│   └── Dockerfile      # Configuración de la imagen del contenedor
├── .env.example        # Plantilla para variables de entorno
├── docker-compose.yml  # Orquestador de servicios (API + Base de Datos)
├── requirements.txt    # Dependencias del proyecto
└── tasks_BD.sql        # Script de inicialización de la base de datos