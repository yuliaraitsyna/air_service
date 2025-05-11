from datetime import date
from random import randint
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.airplane import Airplane
from app.models.airport import Airport
from app.models.flight import Flight
from app.models.passenger import Passenger
from app.models.ticket import Ticket
from app.schemas.airplane import AirplaneCreate
from app.schemas.airport import AirportCreate
from app.schemas.flight import FlightCreate
from app.schemas.passenger import PassengerCreate
from app.schemas.ticket import TicketCreate

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
        
class TicketsNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Tickets not found")
        
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

def generate_free_seat(db: Session, flight_id: int) -> int:
    used_seats = {t.seat_number for t in db.query(Ticket).filter_by(flight_id=flight_id).all()}
    for _ in range(100):
        seat = randint(1, 150)
        if seat not in used_seats:
            return seat
    raise Exception("No free seats available")

def calculate_price(flight: Flight, with_luggage: bool) -> float:
    base_price = flight.price
    if with_luggage:
        return base_price + 20.0
    return base_price

def create_ticket(db: Session, data: TicketCreate, user_id: int) -> Ticket:
    passenger = db.query(Passenger).get(data.passenger_id)
    flight = db.query(Flight).get(data.flight_id)

    if not passenger or not flight:
        raise ValueError("Invalid passenger or flight")

    seat_number = generate_free_seat(db, data.flight_id)
    price = calculate_price(flight, data.with_luggage)

    ticket = Ticket(
        passenger_id=data.passenger_id,
        flight_id=data.flight_id,
        seat_number=seat_number,
        with_luggage=data.with_luggage,
        price=price,
        booked_at=date.today(),
        status="booked",
        user_id = user_id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_tickets(db: Session, skip: int, limit: int):
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    if not tickets:
        raise TicketsNotFoundException()
    return tickets

def get_ticket(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise TicketsNotFoundException()
    return ticket