from uuid import UUID
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    company_id: UUID

class UserModel(UserBase):
    hashed_password: str

class UserCreateModel(UserBase):
    password: str
    
class UserViewModel(UserBase):
    id: UUID
    
    class Config:
        orm_mode = True