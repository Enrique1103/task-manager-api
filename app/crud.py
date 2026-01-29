from sqlalchemy.orm import Session
from app import models, schemas, auth

# --- OPERACIONES DE USUARIOS ---

def get_user_by_email(db: Session, email: str):
    """Busca un usuario por su correo electrónico."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Crea un nuevo usuario con la contraseña hasheada."""
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

# --- OPERACIONES DE TAREAS ---

def get_tasks(db: Session, user_id: int, status: str = None):
    """Obtiene todas las tareas de un usuario específico, con filtro opcional de estado."""
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    if status:
        query = query.filter(models.Task.status == status)
    return query.all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """Crea una tarea asociada a un usuario."""
    # .model_dump() es la forma correcta en Pydantic v2 (reemplaza a .dict())
    # exclude_unset=True hace que SOLO se incluyan los intoducidos
    task_data = task.model_dump(exclude_unset=True)
    
    db_task = models.Task(**task_data, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    """Actualiza una tarea existente si pertenece al usuario logueado."""
    db_task = db.query(models.Task).filter(
        models.Task.id_task == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if not db_task:
        return None

    # exclude_unset=True evita que los campos que no se evian se pongan en NULL
    update_data = task_update.model_dump(exclude_unset=True) 
    
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    """Elimina una tarea si pertenece al usuario logueado."""
    db_task = db.query(models.Task).filter(
        models.Task.id_task == task_id, 
        models.Task.user_id == user_id
    ).first()
    
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False