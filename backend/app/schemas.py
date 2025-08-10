
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "parent"
    full_name: Optional[str]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    full_name: Optional[str]
    class Config:
        orm_mode = True

class StudentIn(BaseModel):
    student_id: str
    data: Dict[str, Any]
