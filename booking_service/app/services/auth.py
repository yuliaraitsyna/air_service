import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from datetime import timedelta
from fastapi import HTTPException, status

load_dotenv()

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

class DatabaseErrorException(HTTPException):
    def __init__(self, detail="Database error occurred"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

def register_user(db: Session, user_data: UserCreate):
    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise UserAlreadyExistsException()

        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password),
            role=user_data.role
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError as e:
        db.rollback()
        raise DatabaseErrorException(detail="Database integrity error. Could be a constraint violation.")
    except Exception as e:
        db.rollback()
        raise DatabaseErrorException(detail=str(e))

def authenticate_user(db: Session, username: str, password: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.password):
            return user
        else:
            raise InvalidCredentialsException()
    
    except Exception as e:
        raise DatabaseErrorException(detail=str(e))

def create_auth_token(user: User):
    try:
        return create_access_token({"sub": user.username}, timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
    except Exception as e:
        raise DatabaseErrorException(detail="Error while generating JWT token.")
