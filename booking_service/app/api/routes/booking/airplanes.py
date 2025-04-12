from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_airplane, get_airplane, get_airplanes, update_airplane, delete_airplane,
)
from typing import List

from app.schemas.airplane import AirplaneCreate, AirplaneResponse, AirplaneUpdate

router = APIRouter()

@router.post("/airplanes/", response_model=AirplaneResponse)
def create_airplane_endpoint(airplane: AirplaneCreate, db: Session = Depends(get_db)):
    return create_airplane(db, airplane)

@router.get("/airplanes/", response_model=List[AirplaneResponse])
def get_airplanes_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_airplanes(db, skip, limit)

@router.get("/airplanes/{airplane_id}", response_model=AirplaneResponse)
def get_airplane_endpoint(airplane_id: int, db: Session = Depends(get_db)):
    return get_airplane(db, airplane_id)

@router.put("/airplanes/{airplane_id}", response_model=AirplaneResponse)
def update_airplane_endpoint(airplane_id: int, airplane: AirplaneUpdate, db: Session = Depends(get_db)):
    return update_airplane(db, airplane_id, airplane.model_dump(exclude_unset=True))

@router.delete("/airplanes/{airplane_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airplane_endpoint(airplane_id: int, db: Session = Depends(get_db)):
    delete_airplane(db, airplane_id)