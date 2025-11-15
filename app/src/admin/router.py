from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from .model import Admin, AdminAuth
from .schema import AdminCreate, AdminResponse
from .controller import get_admin_list
import uuid

router = APIRouter(prefix="/admins", tags=["admins"])

@router.get("/", response_model=AdminResponse)
def list_admin(db: Session = Depends(get_db)):
  return get_admin_list(db)

@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
  try:
    result=  db.query(Admin).filter(Admin.id == admin_id, Admin.status == 1).first()
    if result:
      return {
        "code": 200,
        "message": "successfully fetch data",
        "result": [result]
      }
    else:
      return {
        "code": 404,
        "message": "admin not found",
        "result": []
      }
  except NameError:
    return JSONResponse(
      status_code=200,
      content={
        "code": 500,
        "message": NameError.name,
        "result": []
      }
    )
  except:
    return JSONResponse(
      status_code=200,
      content={
        "code": 500,
        "message": "internal server error",
        "result": []
      }
    )

@router.post("/", response_model=AdminResponse)
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

      auth = AdminAuth(
        id = auth_id,
        admin_id = id,
        password = data.password,
      )
      db.add(auth)
      db.commit()
      db.refresh(admin)
      return {
        "code": 200,
        "message": "successfully add admin",
        "result": []
      }
  except NameError:
    print(NameError)
    return JSONResponse(
      status_code=200,
      content={"code": 500, "message": "something went wrong", "result": []}
    )
  except:
    return JSONResponse(
      status_code=200,
      content={"code": 500, "message": "something went wrong", "result": []}
    )