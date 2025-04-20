from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import Token, UserResponse
from app.services.auth import get_current_user, register_user, authenticate_user
from app.core.database import get_db
from app.core.jwt import create_access_token

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 15

@router.post("/register", response_model=UserResponse)
def register(
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    return register_user(db, username, email, password)

@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/check", response_model=UserResponse)
def auth_check(current_user: Annotated[dict,  Depends(get_current_user)]):
    print(current_user)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return  current_user
    