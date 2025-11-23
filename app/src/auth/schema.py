from pydantic import BaseModel, ConfigDict


class AdminResult (BaseModel):
  id: int
  name: str
  email: str
  profile_picture: str
  role: str

class LoginData (BaseModel):
  email: str
  password: str

class TokenData (BaseModel):
  token: str
  user: AdminResult

class AuthData (LoginData):
  pass

class AuthResponse(BaseModel):
  code: int
  message: str
  result: list[TokenData]
  model_config = ConfigDict(from_attributes=True)
