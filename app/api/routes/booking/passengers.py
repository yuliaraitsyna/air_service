from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_passenger, get_passenger, get_passengers, update_passenger, delete_passenger,
)
from typing import Annotated, List

from app.schemas.passenger import PassengerCreate, PassengerResponse, PassengerUpdate
from app.models.user import User
from app.services.auth import require_role

router = APIRouter()

db_annotated = Annotated[Session, Depends(get_db)]
user_admin_annotated = Annotated[User, Depends(require_role(["admin"]))]

@router.post("/passengers/", response_model=PassengerResponse)
def create_passenger_endpoint(passenger: PassengerCreate, db: db_annotated, user: user_admin_annotated):
    return create_passenger(db, passenger)

@router.get("/passengers/", response_model=List[PassengerResponse])
def get_passengers_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_passengers(db, skip, limit)

@router.get("/passengers/{passenger_id}", response_model=PassengerResponse)
def get_passenger_endpoint(passenger_id: int, db: db_annotated):
    return get_passenger(db, passenger_id)

@router.put("/passengers/{passenger_id}", response_model=PassengerResponse)
def update_passenger_endpoint(passenger_id: int, passenger: PassengerUpdate,  db: db_annotated, user: user_admin_annotated):
    return update_passenger(db, passenger_id, passenger.model_dump(exclude_unset=True))

@router.delete("/passengers/{passenger_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_passenger_endpoint(passenger_id: int,  db: db_annotated, user: user_admin_annotated):
    delete_passenger(db, passenger_id)