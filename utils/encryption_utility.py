from datetime import datetime, timedelta
from jose import jwt
from database.config import jwt_settings
from passlib.context import CryptContext
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from starlette.authentication import AuthenticationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
crypt_context = CryptContext(schemes=["bcrypt"], bcrypt__default_rounds=5, deprecated="auto")


def get_password_hash(password):
    return crypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, jwt_settings.jwt_secret_key, algorithm=jwt_settings.jwt_algorithm)
        return encoded_jwt
    except Exception as e:
        return e


def handle_auth_error(request: Request, exception: AuthenticationError):
    assert isinstance(exception, AuthenticationError)
    return JSONResponse(content={'message': "Could not validate credentials. please Login"}, status_code=401)
