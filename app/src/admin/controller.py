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
    result =  db.query(Admin).filter(*filters).limit(query.limit).offset(offsets)
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
