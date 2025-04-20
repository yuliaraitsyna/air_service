from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.airplane import Airplane
from app.models.airport import Airport
from app.models.flight import Flight
from app.models.passenger import Passenger
from app.models.payment import Payment
from app.schemas.airplane import AirplaneCreate
from app.schemas.airport import AirportCreate
from app.schemas.flight import FlightCreate
from app.schemas.passenger import PassengerCreate
from app.schemas.payment import PaymentCreate

class PaymentNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

class PassengerNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Passenger not found")

class AirplaneNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Airplane not found")

class AirportNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Airport not found")

class FlightNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")

def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    db_payment = Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int) -> Payment:
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise PaymentNotFoundException()
    return payment

def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
    return db.query(Payment).offset(skip).limit(limit).all()

def update_payment(db: Session, payment_id: int, payment_data: dict) -> Payment:
    payment = get_payment(db, payment_id)
    for key, value in payment_data.items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment

def delete_payment(db: Session, payment_id: int) -> None:
    payment = get_payment(db, payment_id)
    db.delete(payment)
    db.commit()

def create_passenger(db: Session, passenger: PassengerCreate) -> Passenger:
    db_passenger = Passenger(**passenger.model_dump())
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger

def get_passenger(db: Session, passenger_id: int) -> Passenger:
    passenger = db.query(Passenger).filter(Passenger.id == passenger_id).first()
    if not passenger:
        raise PassengerNotFoundException()
    return passenger

def get_passengers(db: Session, skip: int = 0, limit: int = 100) -> List[Passenger]:
    return db.query(Passenger).offset(skip).limit(limit).all()

def update_passenger(db: Session, passenger_id: int, passenger_data: dict) -> Passenger:
    passenger = get_passenger(db, passenger_id)
    for key, value in passenger_data.items():
        setattr(passenger, key, value)
    db.commit()
    db.refresh(passenger)
    return passenger

def delete_passenger(db: Session, passenger_id: int) -> None:
    passenger = get_passenger(db, passenger_id)
    db.delete(passenger)
    db.commit()

def create_airplane(db: Session, airplane: AirplaneCreate) -> Airplane:
    db_airplane = Airplane(**airplane.model_dump())
    db.add(db_airplane)
    db.commit()
    db.refresh(db_airplane)
    return db_airplane

def get_airplane(db: Session, airplane_id: int) -> Airplane:
    airplane = db.query(Airplane).filter(Airplane.id == airplane_id).first()
    if not airplane:
        raise AirplaneNotFoundException()
    return airplane

def get_airplanes(db: Session, skip: int = 0, limit: int = 100) -> List[Airplane]:
    return db.query(Airplane).offset(skip).limit(limit).all()

def update_airplane(db: Session, airplane_id: int, airplane_data: dict) -> Airplane:
    airplane = get_airplane(db, airplane_id)
    for key, value in airplane_data.items():
        setattr(airplane, key, value)
    db.commit()
    db.refresh(airplane)
    return airplane

def delete_airplane(db: Session, airplane_id: int) -> None:
    airplane = get_airplane(db, airplane_id)
    db.delete(airplane)
    db.commit()

def create_airport(db: Session, airport: AirportCreate) -> Airport:
    db_airport = Airport(**airport.dict())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport

def get_airport(db: Session, airport_id: int) -> Airport:
    airport = db.query(Airport).filter(Airport.id == airport_id).first()
    if not airport:
        raise AirportNotFoundException()
    return airport

def get_airports(db: Session, skip: int = 0, limit: int = 100) -> List[Airport]:
    return db.query(Airport).offset(skip).limit(limit).all()

def update_airport(db: Session, airport_id: int, airport_data: dict) -> Airport:
    airport = get_airport(db, airport_id)
    for key, value in airport_data.items():
        setattr(airport, key, value)
    db.commit()
    db.refresh(airport)
    return airport

def delete_airport(db: Session, airport_id: int) -> None:
    airport = get_airport(db, airport_id)
    db.delete(airport)
    db.commit()

def create_flight(db: Session, flight: FlightCreate) -> Flight:
    get_airplane(db, flight.airplane_id)
    
    get_airport(db, flight.from_airport_id)
    get_airport(db, flight.to_airport_id)
    
    db_flight = Flight(**flight.model_dump())
    try:
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
    except Exception as e:
        print("Error:", e)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_flight

def get_flight(db: Session, flight_id: int) -> Flight:
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise FlightNotFoundException()
    return flight

def get_flights(db: Session, skip: int = 0, limit: int = 100) -> List[Flight]:
    return db.query(Flight).offset(skip).limit(limit).all()

def update_flight(db: Session, flight_id: int, flight_data: dict) -> Flight:
    flight = get_flight(db, flight_id)
    
    if 'airplane_id' in flight_data:
        get_airplane(db, flight_data['airplane_id'])
    
    if 'from_airport_id' in flight_data:
        get_airport(db, flight_data['from_airport_id'])
    if 'to_airport_id' in flight_data:
        get_airport(db, flight_data['to_airport_id'])
    
    for key, value in flight_data.items():
        setattr(flight, key, value)
    db.commit()
    db.refresh(flight)
    return flight

def delete_flight(db: Session, flight_id: int) -> None:
    flight = get_flight(db, flight_id)
    db.delete(flight)
    db.commit()

# def search_flights(
#     db: Session,
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
#     limit: int = 100
# ) -> List[Flight]:
#     query = db.query(Flight).join(
#         Airport, Flight.from_airport_id == Airport.id
#     ).join(
#         Airport, Flight.to_airport_id == Airport.id,
#         aliased=True
#     )
    
#     if from_airport_id:
#         query = query.filter(Flight.from_airport_id == from_airport_id)
#     if to_airport_id:
#         query = query.filter(Flight.to_airport_id == to_airport_id)
    
#     if departure_date:
#         query = query.filter(Flight.departure_time >= departure_date)
    
#     if from_airport_code:
#         query = query.filter(Airport.code.ilike(f"%{from_airport_code}%"))
#     if to_airport_code:
#         query = query.filter(Airport.code.ilike(f"%{to_airport_code}%"))
    
#     if from_city:
#         query = query.filter(Airport.city.ilike(f"%{from_city}%"))
#     if to_city:
#         query = query.filter(Airport.city.ilike(f"%{to_city}%"))
    
#     if from_country:
#         query = query.filter(Airport.country.ilike(f"%{from_country}%"))
#     if to_country:
#         query = query.filter(Airport.country.ilike(f"%{to_country}%"))
    
#     return query.offset(skip).limit(limit).all() 