import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext


# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Configuración obtenida del entorno
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 3. Validación de seguridad
if not SECRET_KEY:
    raise ValueError("ERROR CRÍTICO: No se encontró la variable 'SECRET_KEY' en el archivo .env")

# Configuración de cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Convierte la contraseña plana en un hash seguro."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Compara la contraseña ingresada con el hash guardado."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Genera un token JWT firmado."""
    to_encode = data.copy()
    # Usamos timezone.utc para evitar el aviso de 'utcnow' depreciado
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)