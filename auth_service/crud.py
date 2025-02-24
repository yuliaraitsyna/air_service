from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse
from security import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        name=user.name,
        surname=user.surname,
        role=user.role.value,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=str(db_user.id),
        username=db_user.username,
        name=db_user.name,
        surname=db_user.surname,
        role=db_user.role.value,
    )

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()