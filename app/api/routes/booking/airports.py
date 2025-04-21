from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_airport, get_airport, get_airports, update_airport, delete_airport,
)
from typing import Annotated, List

from app.schemas.airport import AirportCreate, AirportResponse, AirportUpdate
from app.models.user import User
from app.services.auth import require_role

router = APIRouter()

db_annotated = Annotated[Session, Depends(get_db)]
user_admin_annotated = Annotated[User, Depends(require_role(["admin"]))]

@router.post("/airports", response_model=AirportResponse)
def create_airport_endpoint(airport: AirportCreate,  db: db_annotated, user: user_admin_annotated):
    return create_airport(db, airport)

@router.get("/airports", response_model=List[AirportResponse])
def get_airports_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_airports(db, skip, limit)

@router.get("/airports/{airport_id}", response_model=AirportResponse)
def get_airport_endpoint(airport_id: int, db: db_annotated):
    return get_airport(db, airport_id)

@router.put("/airports/{airport_id}", response_model=AirportResponse)
def update_airport_endpoint(airport_id: int, airport: AirportUpdate, db: db_annotated, user: user_admin_annotated):
    return update_airport(db, airport_id, airport.dict(exclude_unset=True))

@router.delete("/airports/{airport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airport_endpoint(airport_id: int, db: db_annotated, user: user_admin_annotated):
    delete_airport(db, airport_id)