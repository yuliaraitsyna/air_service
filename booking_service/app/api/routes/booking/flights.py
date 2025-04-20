from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_flight, get_flight, get_flights, update_flight, delete_flight
)
from typing import Annotated, List

from app.schemas.flight import FlightCreate, FlightResponse, FlightUpdate
from app.models.user import User
from app.services.auth import require_role

router = APIRouter()

db_annotated = Annotated[Session, Depends(get_db)]
user_admin_annotated = Annotated[User, Depends(require_role(["admin"]))]

@router.post("/flights/", response_model=FlightResponse)
def create_flight_endpoint(flight: FlightCreate, db: db_annotated, user: user_admin_annotated):
    return create_flight(db, flight)

@router.get("/flights/", response_model=List[FlightResponse])
def get_flights_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_flights(db, skip, limit)

@router.get("/flights/{flight_id}", response_model=FlightResponse)
def get_flight_endpoint(flight_id: int, db: db_annotated):
    return get_flight(db, flight_id)

@router.put("/flights/{flight_id}", response_model=FlightResponse)
def update_flight_endpoint(flight_id: int, flight: FlightUpdate, db: db_annotated, user: user_admin_annotated):
    return update_flight(db, flight_id, flight.model_dump(exclude_unset=True))

@router.delete("/flights/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight_endpoint(flight_id: int, db: db_annotated, user: user_admin_annotated):
    delete_flight(db, flight_id)

# @router.get("/flights/search/", response_model=List[FlightResponse])
# def search_flights_endpoint(
#     from_airport_id: Optional[int] = None,
#     to_airport_id: Optional[int] = None,
#     departure_date: Optional[date] = None,
#     from_airport_code: Optional[str] = None,
#     to_airport_code: Optional[str] = None,
#     from_city: Optional[str] = None,
#     to_city: Optional[str] = None,
#     from_country: Optional[str] = None,
#     to_country: Optional[str] = None,
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     return search_flights(
#         db,
#         from_airport_id=from_airport_id,
#         to_airport_id=to_airport_id,
#         departure_date=departure_date,
#         from_airport_code=from_airport_code,
#         to_airport_code=to_airport_code,
#         from_city=from_city,
#         to_city=to_city,
#         from_country=from_country,
#         to_country=to_country,
#         skip=skip,
#         limit=limit
#     ) 