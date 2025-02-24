from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def init():
    return {"description": "API service is running"}
    