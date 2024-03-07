from fastapi import FastAPI, Request
import uvicorn
from api.v1.users.app import public_router
from api.v1.users.app import private_router
from api.v1.users import model
from database.connection import engine
from fastapi.security import OAuth2PasswordBearer
import time
from fastapi_auth_middleware import AuthMiddleware
from utils.encryption_utility import handle_auth_error
from api.v1.users.utility import get_authorised_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

model.Base.metadata.create_all(bind=engine)

public_app = FastAPI(docs_url="/api/docs")
public_app.include_router(public_router, prefix="/user", tags=['users'])


@public_app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    return response


private_app = FastAPI(docs_url="/api/docs")
private_app.include_router(private_router, prefix="/user", tags=['users'])
private_app.add_middleware(
    AuthMiddleware,
    verify_header=get_authorised_user,
    auth_error_handler=handle_auth_error
)


@private_app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    return response


app = FastAPI(docs_url="/api/docs", openapi_url="/openapi.json")
app.mount("/public", public_app)
app.mount("/auth", private_app)


@app.get("/health")
def endpoint_check_health_status():
    return {"success": True}


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8005)  # Starts the uvicorn ASGI
