from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Vehicle(Base):
  __tablename__ = "vehicles"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(200))
  brand = Column(String(200))
  plate_number = Column(String(50), unique=True)