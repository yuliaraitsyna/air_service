from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Login, UserCreate, Token, UserResponse
from app.services.auth import register_user, authenticate_user, create_auth_token
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return register_user(db, user_data)

@router.post("/login", response_model=Token)
def login(user_data: Login, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_auth_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
