import os
from scalar_fastapi import get_scalar_api_reference
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, database, schemas, crud, auth
from jose import jwt, JWTError

app = FastAPI(
    title="Task Manager API",
    description="API robusta con esquemas de PostgreSQL, JWT y validación Pydantic v2",
    version="1.0.0"
)

# CONFIGURACIÓN DE SCALAR 
# Detectamos si estamos en desarrollo (por defecto sí)
os.getenv("ENV", "development") == "development"
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=app.title + " - Docs Profesionales",
        )

# Configuración de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- DEPENDENCIAS ---

def get_db():
    """Generador de sesiones de base de datos."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Inyección de seguridad para validar el token y obtener el usuario."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# --- RUTAS DE AUTENTICACIÓN ---

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.create_user(db, user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales incorrectas"
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- RUTAS DE TAREAS (CRUD) ---

@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return crud.create_task(db, task, user_id=current_user.id_user)


@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(
    status: Optional[schemas.TaskStatus] = None, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Obtiene las tareas del usuario actual. Filtro opcional por estado."""
    return crud.get_tasks(db, user_id=current_user.id_user, status=status)


@app.put("/tasks/{id_task}", response_model=schemas.TaskResponse)
def update_task(
    id_task: int, 
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    updated_task = crud.update_task(db, id_task, task_update, current_user.id_user)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tarea no encontrada o no tienes permiso para editarla"
        )
    return updated_task

@app.delete("/tasks/{id_task}", status_code=status.HTTP_200_OK)
def delete_task(
    id_task: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    success = crud.delete_task(db, id_task, current_user.id_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tarea no encontrada o no tienes permiso para eliminarla"
        )
    return {"message": f"Tarea {id_task} borrada exitosamente"}