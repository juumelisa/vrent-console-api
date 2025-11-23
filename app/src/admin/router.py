from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.public import auth_public
from app.middleware.admin import auth_admin, auth_super_admin
from .model import Admin, AdminAuth
from .schema import AdminCreate, AdminResponse, AdminQuery
from .controller import get_admin_list, get_admin_info
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/admins", tags=["admins"])

@router.get("/", dependencies=[Depends(auth_public), Depends(auth_admin)], response_model=AdminResponse)
def list_admin(query: AdminQuery = Depends(), db: Session = Depends(get_db)):
  return get_admin_list(query, db)

@router.get("/{admin_id}", dependencies=[Depends(auth_public), Depends(auth_admin)], response_model=AdminResponse)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
  return get_admin_info(admin_id, db)

@router.post("/", dependencies=[Depends(auth_public), Depends(auth_super_admin)], response_model=AdminResponse)
def create_admin(data: AdminCreate, db: Session = Depends(get_db)):
  try:
    exist_admin = db.query(Admin).filter(Admin.email == data.email, Admin.status == 1).first()
    if (exist_admin):
      return JSONResponse(
        status_code=200,
        content={
          "code": 400,
          "message": "admin with the same email is exist!",
          "result": []
        }
      )
    else:
      role = 3
      if (data.role == "super admin"):
        role = 1
      elif (data.role == "admin"):
        role = 2

      id = uuid.uuid4().int % 10**12
      auth_id = uuid.uuid4().int % 10**12
      admin = Admin(
        id = id,
        name = data.name.strip().title(),
        email = data.email.strip(),
        profile_picture = data.profile_picture,
        role = role,
      )
      db.add(admin)

      hashPassword = pwd_context.hash(data.password)

# def verify_password(password: str, hashed: str):
#     return pwd_context.verify(password, hashed)
      auth = AdminAuth(
        id = auth_id,
        admin_id = id,
        password = hashPassword,
      )
      
      db.add(auth)
      db.commit()
      db.refresh(admin)
      return {
        "code": 200,
        "message": "successfully add admin",
        "result": []
      }
  except:
    return JSONResponse(
      status_code=200,
      content={"code": 500, "message": "something went wrong", "result": []}
    )