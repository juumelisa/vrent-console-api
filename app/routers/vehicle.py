from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse

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