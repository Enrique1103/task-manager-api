from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base 

class User(Base):
    # Configuración de Tabla Declarativa
    __tablename__ = "users"
    __table_args__ = {"schema": "user_schema"}

    id_user = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    role_name = Column(Text, default="rol_user")

    # Relación: un usuario tiene muchas tareas
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    # Configuración de Tabla Declarativa
    __tablename__ = "tasks"
    __table_args__ = {"schema": "task_schema"}

  
    id_task = Column(Integer, primary_key=True, index=True) 
    tasks_name = Column(String(25), nullable=False)
    created = Column(Date, server_default=func.now())
    status = Column(String(20), nullable=True, default="pendiente")
    # Referencia al esquema y tabla de usuarios
    user_id = Column(Integer, ForeignKey("user_schema.users.id_user", ondelete="CASCADE", onupdate="CASCADE"))

    # Relación inversa
    owner = relationship("User", back_populates="tasks")
