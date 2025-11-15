from sqlalchemy import Column, BigInteger, SmallInteger, String, DateTime, func
from app.config.database import Base

class Admin(Base):
  __tablename__ = "admins"

  id = Column(BigInteger, primary_key=True)
  name = Column(String(200))
  email = Column(String(200), unique=True)
  role = Column(SmallInteger, comment="1:super admin, 2:admin, 3:staff")
  profile_picture = Column(String(500), nullable=True)
  status = Column(SmallInteger, default=1, comment="0:inactive,1:active")
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AdminAuth(Base):
  __tablename__ = "admin_auth"
  id = Column(BigInteger, primary_key=True)
  admin_id = Column(BigInteger, unique=True)
  password = Column(String(200))
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class AdminToken(Base):
  __tablename__ = "admin_token"

  id = Column(BigInteger, primary_key=True)
  admin_id = Column(BigInteger)
  token = Column(String(50))
  expired_date = Column(DateTime)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())