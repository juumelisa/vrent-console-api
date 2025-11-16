from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from .schema import AuthData, AuthResponse
from .controller import auth

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/", response_model=AuthResponse)
def check_auth(data: AuthData, db: Session = Depends(get_db)):
  return auth(data, db)