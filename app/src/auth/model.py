from sqlalchemy import Column, BigInteger, String, DateTime, func
from app.config.database import Base

class AdminToken(Base):
  __tablename__ = "admin_token"

  id = Column(BigInteger, primary_key=True)
  admin_id = Column(BigInteger)
  token = Column(String(64))
  expired_date = Column(DateTime)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())