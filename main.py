from fastapi import FastAPI
from api.v1.users.app import router as user
from api.v1.users import model
from database.connection import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/api/docs",openapi_url="/openapi.json")
app.include_router(user,prefix="/user",tags=['users'])


@app.get("/health")
def endpoint_check_health_status():
    return {"success":True}