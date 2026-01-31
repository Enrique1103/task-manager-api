from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional
from enum import Enum

# --- ENUMS ---
class TaskStatus(str, Enum):
    pendiente = "pendiente"
    completada = "completada"

# --- USUARIOS ---
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr # Valida automáticamente que sea un email real
    role_name: Optional[str] = "rol_user"

class UserCreate(UserBase):
    password_hash: str = Field(..., min_length=6) # En el registro pedimos la contraseña

class UserResponse(UserBase):
    id_user: int

    class Config:
        from_attributes = True # Esto permite a Pydantic leer modelos de SQLAlchemy

# --- TAREAS ---
class TaskBase(BaseModel):
    tasks_name: str = Field(..., min_length=1, max_length=25)
    status: Optional[TaskStatus] = TaskStatus.pendiente

class TaskCreate(TaskBase):
    pass
class TaskUpdate(BaseModel):
    # Todos son opcionales para permitir actualizaciones parciales (PATCH)
    tasks_name: Optional[str] = Field(None, max_length=25)
    status: Optional[TaskStatus] = None
class TaskResponse(TaskBase):
    id_task: int
    user_id: int
    created: date

    class Config:
        from_attributes = True