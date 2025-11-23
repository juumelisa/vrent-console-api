from fastapi import Header, Request, HTTPException
from app.config.database import SessionLocal
from app.src.auth.model import AdminToken
from app.src.admin.model import Admin

async def auth_super_admin(request: Request):
  token = request.headers.get("token")
  if token is None:
    raise HTTPException(
      status_code=401,
      detail={
        "code" :401,
        "message": "unauthorized",
        "result": []
      }
    )
  else:
    db = SessionLocal()
    try:
      tokenData = db.query(AdminToken).filter(
        AdminToken.token == token
      ).first()
      if not tokenData:
        raise HTTPException(
          status_code=401,
          detail={
            "code" :401,
            "message": "unauthorized",
            "result": []
          }
        )
      userData = db.query(Admin).filter(
        Admin.id == tokenData.admin_id,
        Admin.role == 1
      ).first()
      if not userData:
        raise HTTPException(
          status_code=401,
          detail={
            "code" :401,
            "message": "unauthorized",
            "result": []
          }
        )
    except NameError:
      print(NameError)
      raise HTTPException(
        status_code=401,
        detail={
          "code" :500,
          "message": "internal server error",
          "result": []
        }
      )
    finally:
      db.close()
    
    # response = await call_next(request)
    # return response