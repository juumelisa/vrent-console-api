from fastapi import FastAPI
from app.database import Base, engine
from app.routers import vehicle

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vehicle.router)

@app.get("/")
def hello():
  return {
    "code": "400",
    "message": ["Hello, there! i'm learning FastAPI"],
    "result": []
  }