from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.src.admin.model import Admin, AdminAuth
from .schema import AuthData
from .model import AdminToken
import os
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
          return {
            "code": 200,
            "message": "successfully fetch data",
            "result": [{
              "token": token
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
  except NameError:
    print(NameError)
    return JSONResponse(
      status_code=200,
      content={
        "code": 500,
        "message": "internal server error",
        "result": []
      }
    )
