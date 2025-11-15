from pydantic import BaseModel, ConfigDict

class AdminBase (BaseModel):
  name: str
  email: str
  profile_picture: str
  role: str
  password: str
  
class AdminCreate (AdminBase):
  pass

class AdminResult (BaseModel):
  id: int
  name: str
  email: str
  profile_picture: str

class AdminResponse(BaseModel):
  code: int
  message: str
  result: list[AdminResult]
  model_config = ConfigDict(from_attributes=True)
