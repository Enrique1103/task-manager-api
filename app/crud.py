from sqlalchemy.orm import Session
from app import models, schemas, auth

# USUARIOS
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = auth.hash_password(user.password_hash)
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_pw,
        role_name=user.role_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# TAREAS
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    # Extraemos los datos a un diccionario
    task_data = task.dict()
    # Nos aseguramos de que 'user_id' no esté en el diccionario para que no choque
    task_data.pop("user_id", None) 
    
    db_task = models.Task(**task_data, user_id=user_id)
    db.add(db_task)
    db.commit()

    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate, user_id: int):
    # Buscamos la tarea que pertenezca al usuario
    db_task = db.query(models.Task).filter(
        models.Task.id_task == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if not db_task:
        return None

    # Convertimos el esquema a diccionario (usar .dict() para Pydantic v1 o .model_dump() para v2)
    # exclude_unset=True evita que los campos que no enviaste se borren en la DB
    update_data = task_data.dict(exclude_unset=True) 
    
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id_task == task_id, models.Task.user_id == user_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False