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

@router.post(
    "/",
    response_model=PassengerResponse,
    summary="Create a new passenger",
    description="""
Create a new passenger record.  
Only users with the `admin` role can perform this operation.
"""
)
def create_passenger_endpoint(passenger: PassengerCreate, db: db_annotated, user: user_admin_annotated):
    return create_passenger(db, passenger)

@router.get(
    "/",
    response_model=List[PassengerResponse],
    summary="Retrieve all passengers",
    description="""
Returns a list of all passengers.  
Supports pagination using `skip` and `limit` query parameters.
"""
)
def get_passengers_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_passengers(db, skip, limit)

@router.get(
    "/{passenger_id}",
    response_model=PassengerResponse,
    summary="Get passenger by ID",
    description="Retrieve detailed information about a specific passenger by their ID."
)
def get_passenger_endpoint(passenger_id: int, db: db_annotated):
    return get_passenger(db, passenger_id)

@router.put(
    "/{passenger_id}",
    response_model=PassengerResponse,
    summary="Update passenger information",
    description="""
Update fields of a specific passenger by their ID.  
Only users with the `admin` role can update passenger records.  
Only fields provided in the request will be updated.
"""
)
def update_passenger_endpoint(passenger_id: int, passenger: PassengerUpdate, db: db_annotated, user: user_admin_annotated):
    return update_passenger(db, passenger_id, passenger.model_dump(exclude_unset=True))

@router.delete(
    "/{passenger_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a passenger",
    description="""
Delete a passenger by their ID.  
Only users with the `admin` role can delete passenger records.
"""
)
def delete_passenger_endpoint(passenger_id: int, db: db_annotated, user: user_admin_annotated):
    delete_passenger(db, passenger_id)
