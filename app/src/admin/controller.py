from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from .model import Admin

def get_admin_list(db: Session):
  try:
    result =  db.query(Admin).filter(
      Admin.status == 1
    )
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
