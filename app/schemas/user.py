from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    fname: str
    lname: str
    email: str
    hashedpw: str
    role: str

class UserUpdateCurrent(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    password: Optional[str] = None


