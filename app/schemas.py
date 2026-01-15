from pydantic import BaseModel
from datetime import date
from typing import Optional

# --- USUARIOS ---
class UserBase(BaseModel):
    full_name: str
    email: str
    password_hash: str
    role_name: Optional[str] = "rol_user"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id_user: int
    class Config:
        from_attributes = True

# --- TAREAS ---
class TaskBase(BaseModel):
    tasks_name: str
    created: Optional[date] = None
    status: Optional[str] = "pendiente"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    tasks_name: Optional[str] = None
    created: Optional[date] = None
    status: Optional[str] = None

class TaskResponse(TaskBase):
    id_task: int
    user_id: int
    class Config:
        from_attributes = True