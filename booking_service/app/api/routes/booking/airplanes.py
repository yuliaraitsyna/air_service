from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (create_airplane, get_airplane, get_airplanes, update_airplane, delete_airplane)
from app.schemas.airplane import AirplaneCreate, AirplaneResponse, AirplaneUpdate
from app.models.user import User
from app.services.auth import require_role
from typing import Annotated, List

router = APIRouter()

db_annotated = Annotated[Session, Depends(get_db)]
user_admin_annotated = Annotated[User, Depends(require_role(["admin"]))]

@router.post("/airplanes", response_model=AirplaneResponse)
def create_airplane_endpoint(airplane: AirplaneCreate, db: db_annotated, user: user_admin_annotated):
    return create_airplane(db, airplane)

@router.get("/airplanes", response_model=List[AirplaneResponse])
def get_airplanes_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_airplanes(db, skip, limit)

@router.get("/airplanes/{airplane_id}", response_model=AirplaneResponse)
def get_airplane_endpoint(airplane_id: int, db: db_annotated):
    return get_airplane(db, airplane_id)

@router.put("/airplanes/{airplane_id}", response_model=AirplaneResponse)
def update_airplane_endpoint(airplane_id: int, airplane: AirplaneUpdate, db: db_annotated, user: user_admin_annotated):
    return update_airplane(db, airplane_id, airplane.model_dump(exclude_unset=True))

@router.delete("/airplanes/{airplane_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airplane_endpoint(airplane_id: int, db: db_annotated, user: user_admin_annotated):
    delete_airplane(db, airplane_id)