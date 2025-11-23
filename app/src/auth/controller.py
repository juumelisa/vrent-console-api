from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.src.admin.model import Admin, AdminAuth
from .schema import AuthData
from .model import AdminToken
import uuid
from datetime import datetime, timedelta
import secrets

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth(data: AuthData, db: Session):
  try:
    admin =  db.query(Admin).filter(
      Admin.email == data.email,
      Admin.status == 1
    ).first()
    if (admin):
      authData = db.query(AdminAuth).filter(
        AdminAuth.admin_id == admin.id
      ).first()
      if (authData):
        hashPassword = authData.password
        isSamePassword = pwd_context.verify(data.password, hashPassword)
        if isSamePassword:
          expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
          token = secrets.token_hex(32)
          id = uuid.uuid4().int % 10**12
          db.query(AdminToken).filter(AdminToken.admin_id == admin.id).delete()
          tokenData = AdminToken(
            id = id,
            admin_id = admin.id,
            token = token,
            expired_date = expire
          )
          db.add(tokenData)
          db.commit()
          db.refresh(tokenData)
          role = "staff"
          if admin.role == 1:
            role = "super admin"
          elif admin.role == 2:
            role = "admin"
          userData = {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
            "profile_picture": admin.profile_picture,
            "role": role
          }
          return {
            "code": 200,
            "message": "logged in",
            "result": [{
              "token": token,
              "user": userData
            }]
          }
        else:
          return {
            "code": 401,
            "message": "invalid credentials!",
            "result": []
          }
      else:
        return {
          "code": 401,
          "message": "invalid credentials!",
          "result": []
        }
    else:
      return {
        "code": 401,
        "message": "invalid credentials!",
        "result": []
      }
  except:
    return JSONResponse(
      status_code=200,
      content={
        "code": 500,
        "message": "internal server error",
        "result": []
      }
    )

def info (token: str, db:Session):
  try:
    isValid = False
    result = []
    if token:
      tokenData = db.query(AdminToken).filter(
        AdminToken.token == token
      ).first()
      if tokenData:
        userData = db.query(Admin).filter(
          Admin.id == tokenData.admin_id
        ).first()
        if userData:
          role = "staff"
          if userData.role == 1:
            role = "super admin"
          elif userData.role == 2:
            role = "admin"
          profile_picture = ""
          if (userData.profile_picture and userData.profile_picture.startswith("https")):
            profile_picture = userData.profile_picture
          obj = {
            "id": userData.id,
            "name": userData.name,
            "email": userData.email,
            "profile_picture": profile_picture,
            "role": role
          }
          isValid = True
          result = [obj]
    if isValid:
      return {
        "code": 200,
        "message": "successfully fetch user information",
        "result": result
      }
    else:
      return {
        "code": 401,
        "message": "invalid credentials!",
        "result": []
      }
  except:
    return {
      "code": 500,
      "message": "internal server error",
      "result": []
    }

def remove_token(token: str, db: Session):
  try:
    if not token:
      return {
        "code": 401,
        "message": "invalid credentials!",
        "result": []
      }
    else:
      tokenData = db.query(AdminToken).filter(
        AdminToken.token == token
      ).first()
      if (tokenData):
        db.delete(tokenData)
        db.commit()
        return {
          "code": 200,
          "message": "successfully logout!",
          "result": []
        }
      else:
        return {
          "code": 401,
          "message": "invalid credentials!",
          "result": []
        }
  except:
    return {
      "code": 500,
      "message": "internal server error",
      "result": []
    }