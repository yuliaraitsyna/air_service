from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_passenger, get_passenger, get_passengers, update_passenger, delete_passenger,
)
from typing import Optional, List
from datetime import date

from app.models.passenger import Passenger
from app.schemas.passenger import PassengerCreate, PassengerResponse, PassengerUpdate

router = APIRouter()

@router.post("/passengers/", response_model=PassengerResponse)
def create_passenger_endpoint(passenger: PassengerCreate, db: Session = Depends(get_db)):
    return create_passenger(db, passenger)

@router.get("/passengers/", response_model=List[PassengerResponse])
def get_passengers_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_passengers(db, skip, limit)

@router.get("/passengers/{passenger_id}", response_model=PassengerResponse)
def get_passenger_endpoint(passenger_id: int, db: Session = Depends(get_db)):
    return get_passenger(db, passenger_id)

@router.put("/passengers/{passenger_id}", response_model=PassengerResponse)
def update_passenger_endpoint(passenger_id: int, passenger: PassengerUpdate, db: Session = Depends(get_db)):
    return update_passenger(db, passenger_id, passenger.model_dump(exclude_unset=True))

@router.delete("/passengers/{passenger_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_passenger_endpoint(passenger_id: int, db: Session = Depends(get_db)):
    delete_passenger(db, passenger_id)