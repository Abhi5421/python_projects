from pydantic import BaseModel, EmailStr, model_validator, ConfigDict
from typing import Optional, Any
import re


class NewUser(BaseModel):
    email: EmailStr
    password: str

    @model_validator(mode="before")
    @classmethod
    def check_input_data(cls, data: Any) -> Any:
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$"
        if not re.match(pattern, data['password']):
            raise ValueError("Password does not meet the required criteria")
        return data


class UpdateUserModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[int] = None
    is_active: Optional[bool] = None
