from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.config.database import get_db
from .model import Admin
from .schema import AdminQuery

def get_admin_list(query: AdminQuery, db: Session):
  try:
    q = query.q
    offsets = (query.page - 1) * query.limit
    filters = [Admin.status == 1]
    if (q):
       filters.append(or_(
          Admin.name.contains(q),
          Admin.email.contains(q)
       ))
    adminList =  db.query(Admin).filter(*filters).limit(query.limit).offset(offsets)
    result = []
    for index, admin in enumerate(adminList):
      role = "staff"
      if admin.role == 1:
        role = "super admin"
      elif admin.role == 2:
        role = "admin"

      profile_picture = ""
      if (admin.profile_picture and admin.profile_picture.startswith("https")):
        profile_picture = admin.profile_picture
      obj = {
        "id": admin.id,
        "name": admin.name,
        "email": admin.email,
        "profile_picture": profile_picture,
        "role": role
      }
      result.append(obj)
    return {
      "code": 200,
      "message": "successfully fetch data",
      "result": result
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
