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

@router.post(
    "/",
    response_model=AirplaneResponse,
    summary="Create a new airplane",
    description="""
Create a new airplane in the system.  
Only users with the `admin` role are allowed to perform this action.
"""
)
def create_airplane_endpoint(airplane: AirplaneCreate, db: db_annotated, user: user_admin_annotated):
    return create_airplane(db, airplane)

@router.get(
    "/",
    response_model=List[AirplaneResponse],
    summary="Get list of airplanes",
    description="""
Retrieve a list of all airplanes.  
Supports pagination with `skip` and `limit` query parameters.
"""
)
def get_airplanes_endpoint(db: db_annotated, skip: int = 0, limit: int = 100):
    return get_airplanes(db, skip, limit)

@router.get(
    "/{airplane_id}",
    response_model=AirplaneResponse,
    summary="Get a single airplane",
    description="""
Retrieve the details of a specific airplane by its ID.
"""
)
def get_airplane_endpoint(airplane_id: int, db: db_annotated):
    return get_airplane(db, airplane_id)

@router.put(
    "/{airplane_id}",
    response_model=AirplaneResponse,
    summary="Update an airplane",
    description="""
Update the data of an existing airplane.  
Only users with the `admin` role are allowed to perform this action.  
Only the provided fields will be updated.
"""
)
def update_airplane_endpoint(airplane_id: int, airplane: AirplaneUpdate, db: db_annotated, user: user_admin_annotated):
    return update_airplane(db, airplane_id, airplane.model_dump(exclude_unset=True))

@router.delete(
    "/{airplane_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an airplane",
    description="""
Delete an airplane from the system by its ID.  
Only users with the `admin` role are allowed to perform this action.
"""
)
def delete_airplane_endpoint(airplane_id: int, db: db_annotated, user: user_admin_annotated):
    delete_airplane(db, airplane_id)