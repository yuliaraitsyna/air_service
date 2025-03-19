from fastapi import FastAPI

app = FastAPI(title="Flight Booking Microservice")

@app.get("/")
def root():
    return {"message": "Flight Booking Service is running"}