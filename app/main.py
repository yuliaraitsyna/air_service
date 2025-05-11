import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth
from app.api.routes import booking

app = FastAPI(title="Flight Booking Microservice")

origins = [
    os.getenv("LOCAL_DEV_URL"),  # React dev server
    os.getenv("PROD_URL"),  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(booking.router, prefix="/booking")

@app.get("/")
def root():
    return {"message": "Flight Booking Service is running"}