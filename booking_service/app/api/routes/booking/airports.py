from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_airport, get_airport, get_airports, update_airport, delete_airport,
)
from typing import List

from app.schemas.airport import AirportCreate, AirportResponse, AirportUpdate

router = APIRouter()

@router.post("/airports/", response_model=AirportResponse)
def create_airport_endpoint(airport: AirportCreate, db: Session = Depends(get_db)):
    return create_airport(db, airport)

@router.get("/airports/", response_model=List[AirportResponse])
def get_airports_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_airports(db, skip, limit)

@router.get("/airports/{airport_id}", response_model=AirportResponse)
def get_airport_endpoint(airport_id: int, db: Session = Depends(get_db)):
    return get_airport(db, airport_id)

@router.put("/airports/{airport_id}", response_model=AirportResponse)
def update_airport_endpoint(airport_id: int, airport: AirportUpdate, db: Session = Depends(get_db)):
    return update_airport(db, airport_id, airport.dict(exclude_unset=True))

@router.delete("/airports/{airport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airport_endpoint(airport_id: int, db: Session = Depends(get_db)):
    delete_airport(db, airport_id)