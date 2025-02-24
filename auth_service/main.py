import schemas

from fastapi import FastAPI
from database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from crud import create_user, get_user_by_username
from security import create_access_token, verify_password

get_db()

app = FastAPI()

@app.get("/")
def init():
    return {"description": "API service is running"}

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    new_user = create_user(db, user)
    return new_user
    
@app.post("/login")
def login(request: schemas.UserLoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user found")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password or username")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    
    return {
        "message": "Login successful", 
        "username": user.username,
        "access_token": access_token,
        "token_type": "bearer"
    }