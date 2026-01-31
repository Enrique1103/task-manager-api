import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar las variables del archivo .env
# Esto busca el archivo .env un nivel arriba (en la raíz del proyecto)
load_dotenv()

# Obtener la URL de conexión
DATABASE_URL = os.getenv("DATABASE_URL")

# Validación de seguridad: Si no existe la variable, detenemos el programa
if not DATABASE_URL:
    raise ValueError("ERROR CRÍTICO: No se encontró la variable 'DATABASE_URL' en el archivo .env")

# Creación del motor de base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica si la conexión está viva antes de usarla
    pool_recycle=3600,   # Reinicia conexiones viejas
    connect_args={"connect_timeout": 10} # Espera hasta 10 segundos si la BD está ocupada
    )

# Creación de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()