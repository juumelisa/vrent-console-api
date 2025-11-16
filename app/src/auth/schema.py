from pydantic import BaseModel, ConfigDict

class LoginData (BaseModel):
  email: str
  password: str

class TokenData (BaseModel):
  token: str

class AuthData (LoginData):
  pass

class AuthResponse(BaseModel):
  code: int
  message: str
  result: list[TokenData]
  model_config = ConfigDict(from_attributes=True)
