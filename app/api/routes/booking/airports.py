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

@router.post(
    "/",
    response_model=AirportResponse,
    summary="Create a new airport",
    description="""
Create a new airport in the system.  
Only users with the `admin` role are allowed to perform this operation.
"""
)
def create_airport_endpoint(airport: AirportCreate, db: db_annotated, user: user_admin_annotated):
    return create_airport(db, airport)

@router.get(
    "/",
    response_model=List[AirportResponse],
    summary="Retrieve all airports",
    description="""
Get a paginated list of all airports.  
You can use `skip` and `limit` query parameters for pagination.
"""
)
def get_airports_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_airports(db, skip, limit)

@router.get(
    "/{airport_id}",
    response_model=AirportResponse,
    summary="Retrieve an airport by ID",
    description="""
Get details of a specific airport by its unique ID.
"""
)
def get_airport_endpoint(airport_id: int, db: db_annotated):
    return get_airport(db, airport_id)

@router.put(
    "/{airport_id}",
    response_model=AirportResponse,
    summary="Update airport information",
    description="""
Update the information of an existing airport.  
Only users with the `admin` role are allowed to perform this operation.  
Only fields provided in the request will be updated.
"""
)
def update_airport_endpoint(airport_id: int, airport: AirportUpdate, db: db_annotated, user: user_admin_annotated):
    return update_airport(db, airport_id, airport.dict(exclude_unset=True))

@router.delete(
    "/{airport_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an airport",
    description="""
Delete an airport from the system by its ID.  
Only users with the `admin` role are allowed to perform this operation.
"""
)
def delete_airport_endpoint(airport_id: int, db: db_annotated, user: user_admin_annotated):
    delete_airport(db, airport_id)
