from fastapi import FastAPI

from app.api.routes import auth
from app.api.routes import booking

app = FastAPI(title="Flight Booking Microservice")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(booking.router, prefix="/booking")

@app.get("/")
def root():
    return {"message": "Flight Booking Service is running"}