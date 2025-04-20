from typing import Annotated
from fastapi import APIRouter, Depends
from pytest import Session

from app.core.database import get_db
from app.models.user import User
from app.services.auth import require_role
from . import payments, passengers, airplanes, airports, flights

router = APIRouter()

router.include_router(airplanes.router, prefix="/airplanes", tags=["Airplanes"])
router.include_router(airports.router, prefix="/airports", tags=["Airports"])
router.include_router(flights.router, prefix="/flights", tags=["Flights"])
router.include_router(passengers.router, prefix="/passengers", tags=["Passengers"])
router.include_router(payments.router,  prefix="/payments", tags=["Payments"])