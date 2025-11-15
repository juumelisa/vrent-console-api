from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from .model import Vehicle
from .schema import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
  v = Vehicle(**data.dict())
  db.add(v)
  db.commit()
  db.refresh(v)
  return v

@router.get("/", response_model=list[VehicleResponse])
def list_vehicles(db: Session = Depends(get_db)):
  return db.query(Vehicle).all()