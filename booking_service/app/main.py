from fastapi import FastAPI

from app.api.routes import auth

app = FastAPI(title="Flight Booking Microservice")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Flight Booking Service is running"}