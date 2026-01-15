from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, database, schemas, crud, auth
from jose import jwt, JWTError

app = FastAPI(title="Task Manager API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependencia de conexión a DB
def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

# Inyección de seguridad para obtener el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="No se pudo validar credenciales"
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None: raise credentials_exception
    except JWTError: raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None: raise credentials_exception
    return user

# --- RUTAS DE AUTENTICACIÓN ---

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_user(db, user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Datos incorrectos")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- RUTAS DE TAREAS (CRUD) ---

@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_tasks(db, user_id=current_user.id_user)

@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_task(db, task, user_id=current_user.id_user)

@app.put("/tasks/{id_task}", response_model=schemas.TaskResponse)
def update_task(
    id_task: int, 
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    updated = crud.update_task(db, id_task, task_update, current_user.id_user)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o no autorizada")
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id, current_user.id_user)
    if not deleted: 
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Borrada correctamente"}