from fastapi import APIRouter

from . import payments, passengers, airplanes, airports, flights

router = APIRouter()

router.include_router(airplanes.router, prefix="/airplanes", tags=["Airplanes"])
router.include_router(airports.router, prefix="/airports", tags=["Airports"])
router.include_router(flights.router, prefix="/flights", tags=["Flights"])
router.include_router(passengers.router, prefix="/passengers", tags=["Passengers"])
router.include_router(payments.router,  prefix="/payments", tags=["Payments"])