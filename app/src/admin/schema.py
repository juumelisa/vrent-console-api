from pydantic import BaseModel, ConfigDict
from typing import Optional
class AdminBase (BaseModel):
  name: str
  email: str
  profile_picture: str
  role: str
  password: str


class AdminQuery(BaseModel):
  q: Optional[str] = None
  limit: int = 10
  page: int = 1

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
