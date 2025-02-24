import schemas

from fastapi import FastAPI
from database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from crud import create_user, get_user_by_username

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
    