from fastapi import Header, HTTPException
import os

def auth_public(x_api_key: str = Header(None)):
  api_key = os.getenv("API_KEY")
  if x_api_key != api_key:
    raise HTTPException(
      status_code=401,
      detail={
        "code" :401,
        "message": "unauthorized",
        "result": []
      }
    )