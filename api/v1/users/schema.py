from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: int
    name: str
    email: str
    mobile: Optional[int]
    is_active: bool

