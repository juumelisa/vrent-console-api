from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.public import auth_public
from .model import Vehicle
from .schema import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", dependencies=[Depends(auth_public)], response_model=VehicleResponse)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
  v = Vehicle(**data.dict())
  db.add(v)
  db.commit()
  db.refresh(v)
  return v

@router.get("/", dependencies=[Depends(auth_public)], response_model=list[VehicleResponse])
def list_vehicles(db: Session = Depends(get_db)):
  return db.query(Vehicle).all()