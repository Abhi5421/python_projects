from pydantic import BaseModel, EmailStr
from typing import Optional


class NewUser(BaseModel):
    email: EmailStr
    password: str


class UpdateUserModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[int] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
