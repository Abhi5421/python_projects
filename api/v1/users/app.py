from fastapi import APIRouter, Depends, UploadFile, File
from api.v1.users.utility import *
from api.v1.users.schema import NewUser, UpdateUserModel
from sqlalchemy.orm import Session
from database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
from utils.logger import create_logger
import os
from utils.celery_task import celery, process_image
from celery.result import AsyncResult

logging = create_logger(__name__)
public_router = APIRouter()
private_router = APIRouter()


@public_router.post("/sign-up")
async def endpoint_sign_up(
        data: NewUser,
        db: Session = Depends(get_db)
):
    try:
        response = await sign_up(data, db)
        return response
    except Exception as e:
        logging.error(e)
        return e


@public_router.post("/sign-in")
async def endpoint_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)

):
    try:
        response = await log_in(form_data, db)
        return response
    except Exception as e:
        logging.error(e)
        return e


@private_router.get("/get-detail/{user_id}")
async def endpoint_get_user_detail(
        user_id: int,
        db: Session = Depends(get_db)
):
    try:
        response = await user_detail(user_id, db)
        return response
    except Exception as e:
        logging.error(e)
        return e


@private_router.get("/get-list")
async def endpoint_get_users_list(
        db: Session = Depends(get_db)
):
    try:
        response = await users_list(db)
        return response
    except Exception as e:
        logging.error(e)
        return e


@private_router.post("/delete/{user_id}")
async def endpoint_delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    try:
        response = await delete_user(user_id, db)
        return response
    except Exception as e:
        logging.error(e)
        return e


@private_router.post("/update-detail/{user_id}")
async def endpoint_update_user_detail(
        user_id: int,
        data: UpdateUserModel,
        db: Session = Depends(get_db)
):
    try:
        response = await update_user(user_id, data, db)
        return response
    except Exception as e:
        logging.error(e)
        return e


# celery endpoints

@public_router.post('/upload/')
async def upload_image(
        file: UploadFile = File(...)
):
    file_path = os.path.join('static/uploads', file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    # Trigger Celery task for image processing
    task = process_image.delay(file_path, 'static/processed')

    return {'task_id': task.id, 'message': 'Image processing started'}


@public_router.get('/task-status/{task_id}')
async def task_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        if result.successful():
            return {'status': 'COMPLETED', 'result': result.get()}
        else:
            return {'status': 'FAILED', 'message': str(result.result)}
    else:
        return {'status': 'PENDING'}
