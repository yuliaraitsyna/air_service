import os
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from fastapi import Depends, HTTPException, status
import jwt

from app.core.database import get_db
from app.core.security import hash_password, verify_password


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

class DatabaseErrorException(HTTPException):
    def __init__(self, detail="Database error occurred"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


def register_user(db: Session, username: str, email: str, password: str, role: str = 'user'):
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise UserAlreadyExistsException()

        user = User(
            username=username,
            email=email,
            password=hash_password(password),
            role=role
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


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: int = payload.get("role")
        
        if username is None or user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "user_id": user_id, "role": role}
    except (ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role(required_roles: list[str]):
    def role_checker(current_user: Annotated[User, Depends(get_current_user)]):
        print(current_user)
        if current_user["role"] not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource."
            )
        return current_user
    return role_checker