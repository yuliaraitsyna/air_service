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

@router.post(
    "/",
    response_model=FlightResponse,
    summary="Create a new flight",
    description="""
Create a new flight with details such as departure/arrival time, airport, and airplane ID.  
Only users with the `admin` role can perform this operation.
"""
)
def create_flight_endpoint(flight: FlightCreate, db: db_annotated, user: user_admin_annotated):
    return create_flight(db, flight)

@router.get(
    "/",
    response_model=List[FlightResponse],
    summary="Retrieve all flights",
    description="""
Returns a paginated list of all available flights.  
Use `skip` and `limit` query parameters to control pagination.
"""
)
def get_flights_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_flights(db, skip, limit)

@router.get(
    "/{flight_id}",
    response_model=FlightResponse,
    summary="Get flight by ID",
    description="""
Retrieve detailed information about a specific flight by its ID.
"""
)
def get_flight_endpoint(flight_id: int, db: db_annotated):
    return get_flight(db, flight_id)

@router.put(
    "/{flight_id}",
    response_model=FlightResponse,
    summary="Update flight details",
    description="""
Update fields of an existing flight by its ID.  
Only users with the `admin` role can update flight details.  
Only fields provided in the request will be updated.
"""
)
def update_flight_endpoint(flight_id: int, flight: FlightUpdate, db: db_annotated, user: user_admin_annotated):
    return update_flight(db, flight_id, flight.model_dump(exclude_unset=True))

@router.delete(
    "/{flight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a flight",
    description="""
Delete a flight by its ID.  
Only users with the `admin` role can delete flights.
"""
)
def delete_flight_endpoint(flight_id: int, db: db_annotated, user: user_admin_annotated):
    delete_flight(db, flight_id)
