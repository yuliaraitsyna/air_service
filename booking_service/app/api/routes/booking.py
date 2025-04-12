from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking import (
    create_payment, get_payment, get_payments, update_payment, delete_payment,
    create_passenger, get_passenger, get_passengers, update_passenger, delete_passenger,
    create_airplane, get_airplane, get_airplanes, update_airplane, delete_airplane,
    create_airport, get_airport, get_airports, update_airport, delete_airport,
    create_flight, get_flight, get_flights, update_flight, delete_flight, search_flights
)
from typing import Optional, List
from datetime import date

from app.models.airport import Airport
from app.models.flight import Flight
from app.models.passenger import Passenger
from app.models.payment import Payment
from app.schemas.airport import AirportCreate, AirportUpdate
from app.schemas.flight import FlightCreate, FlightUpdate
from app.schemas.passenger import PassengerCreate, PassengerResponse, PassengerUpdate
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate
from app.models.airplane import Airplane
from app.schemas.airplane import AirplaneCreate, AirplaneUpdate

# router = APIRouter()

# # Flight routes
# @router.post("/flights/", response_model=Flight)
# def create_flight_endpoint(flight: FlightCreate, db: Session = Depends(get_db)):
#     return create_flight(db, flight)

# @router.get("/flights/", response_model=List[Flight])
# def get_flights_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return get_flights(db, skip, limit)

# @router.get("/flights/{flight_id}", response_model=Flight)
# def get_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
#     return get_flight(db, flight_id)

# @router.put("/flights/{flight_id}", response_model=Flight)
# def update_flight_endpoint(flight_id: int, flight: FlightUpdate, db: Session = Depends(get_db)):
#     return update_flight(db, flight_id, flight.dict(exclude_unset=True))

# @router.delete("/flights/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_flight_endpoint(flight_id: int, db: Session = Depends(get_db)):
#     delete_flight(db, flight_id)

# @router.get("/flights/search/", response_model=List[Flight])
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