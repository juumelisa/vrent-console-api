from fastapi import Request, HTTPException
import os

def auth_public(request: Request):
  api_key = os.getenv("API_KEY")
  x_api_key = request.headers.get("x-api-key")
  if x_api_key != api_key:
    raise HTTPException(
      status_code=401,
      detail={
        "code" :401,
        "message": "unauthorized",
        "result": []
      }
    )