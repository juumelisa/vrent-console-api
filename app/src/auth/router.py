from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.public import auth_public
from .schema import AuthData, AuthResponse
from .controller import auth, remove_token, info
from app.src.admin.schema import AdminResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/", dependencies=[Depends(auth_public)], response_model=AuthResponse)
def check_auth(data: AuthData, db: Session = Depends(get_db)):
  return auth(data, db)

@router.get("/info", dependencies=[Depends(auth_public)], response_model=AdminResponse)
def get_admin(token: str = Header(None), db: Session = Depends(get_db)):
  return info(token, db)


@router.post("/logout", dependencies=[Depends(auth_public)], response_model=AuthResponse)
def logout(authorization: str = Header(None), db: Session = Depends(get_db)):
  return remove_token(authorization, db)