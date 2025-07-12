# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.crud import user as crud_user
from app.api.v1 import schemas
from app.core import security
from app.core.config import settings

from app.core.security import get_current_user
from app.db import models

# Importar el cliente de notificaciones
from notification_client import send_welcome_email_async

router = APIRouter()  # ✅ solo una vez

@router.post("/register", response_model=schemas.UserOut)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear el usuario en la base de datos
    new_user = crud_user.create_user(db=db, user=user_in)
    
    # Verificar que el usuario se creó correctamente
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    # Enviar notificación de bienvenida de forma asíncrona
    try:
        send_welcome_email_async(
            user_name=new_user.name,
            user_email=new_user.email
        )
        print(f"✅ Notificación de bienvenida enviada a {new_user.email}")
    except Exception as e:
        print(f"❌ Error enviando notificación de bienvenida: {e}")
        # No fallar el registro si la notificación falla
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # Aquí se protege
):
    return crud_user.get_all_users(db)

@router.get("/user", response_model=schemas.UserOut)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # Protección con token
):
    db_user = crud_user.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user
