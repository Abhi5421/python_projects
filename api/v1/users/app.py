from fastapi import APIRouter,Depends
from api.v1.users.utility import *
from api.v1.users.schema import User
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database.connection import get_db

router = APIRouter()

@router.post("/sign-in")
async def endpoint_sign_in(
    data: User,
    db: Session = Depends(get_db)
):  
    json_data = jsonable_encoder(data)
    response = await sign_in(json_data,db)
    return response

@router.post("/login")
async def endpoint_login():
    pass

@router.get("/get-detail")
async def endpoint_get_user_detail():
    pass

@router.get("/get-list")
async def endpoint_get_users_list():
    pass