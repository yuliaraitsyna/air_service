from fastapi import FastAPI
from database import check_db_connection

app = FastAPI()

print(check_db_connection)

@app.get("/")
def db_check():
    if check_db_connection():
        return {"status": "ok", "message": "Database connected successfully!"}
    else:
        return {"status": "error", "message": "Database connection failed!"}
