from api.v1.users.model import User
from api.v1.users.schema import NewUser, UpdateUserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.encryption_utility import *
from typing import Union
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer
from database.config import jwt_settings
from database.connection import SessionLocal
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def sign_up(data: NewUser, db: Session):
    exists, user = check_if_user_exists(data.email, db)
    if exists:
        return HTTPException(status_code=500, detail="user already exists, try login")
    result = User(email=data.email,
                  password=get_password_hash(data.password))
    db.add(result)
    db.commit()
    return {"message": "User created successfully!"}


async def get_authorised_user(token: str = Depends(oauth2_scheme)):
    try:
        token = token["authorization"].split(" ")[1]
        payload = jwt.decode(token, jwt_settings.jwt_secret_key, algorithms=[jwt_settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            return False
    except JWTError:
        return False
    db = SessionLocal()
    is_exist, user = check_if_user_exists(email, db)
    if is_exist is None:
        return False
    user = user.user_json()
    scopes = user.get("name")
    return scopes,user


def check_if_user_exists(data: Union[str, int], db: Session):
    if isinstance(data, str):
        user = db.query(User).filter(User.email == data).first()
    else:
        user = db.query(User).filter(User.user_id == data).first()
    if user:
        return True, user
    return False, None


async def log_in(form_data, db):
    email = form_data.username
    password = form_data.password
    if authenticate(email, password, db):
        access_token = create_access_token(
            data={"sub": email}, expires_delta=timedelta(minutes=30))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return HTTPException(
            status_code=400, detail="Incorrect username or password")


def authenticate(email, password, db):
    is_exist, user = check_if_user_exists(email, db)
    if is_exist:
        user = user.user_json()
        password_check = verify_password(password, user['password'])
        if password_check:
            return password_check


async def update_user(user_id: int, data: UpdateUserModel, db: Session):
    exists, user = check_if_user_exists(user_id, db)
    if exists:
        update_data = data.dict(exclude_unset=True)
        db.query(User).filter(User.user_id == user_id).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(user)
        return user


async def user_detail(user_id: int, db: Session):
    is_exist, user = check_if_user_exists(user_id, db)
    if is_exist:
        user = user.user_json()
        del user['password']
        return user
    return HTTPException(
        status_code=400, detail="User doesn't exist")


async def users_list():
    pass
