from api.v1.users.model import User
from sqlalchemy.orm import Session

async def sign_in(data:dict,db:Session):
    result = User(**data)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

async def log_in():
    pass

async def user_deatil():
    pass

async def users_list():
    pass