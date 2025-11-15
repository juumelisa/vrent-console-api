from pydantic import BaseModel

class VehicleBase (BaseModel):
  name: str
  brand: str
  plate_number: str

class VehicleCreate(VehicleBase):
  pass

class VehicleResponse(VehicleBase):
  id: int

  class Config:
    orm_model = True