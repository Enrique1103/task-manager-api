from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, schemas

app = FastAPI()

# Crear tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para obtener sesión
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API conectada a PostgreSQL"}


# Crear usuario
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Listar usuarios
@app.get("/users/", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Crear tarea
@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Listar tareas
@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()
