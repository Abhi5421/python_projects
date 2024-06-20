from sqlalchemy import create_engine
import motor.motor_asyncio
import redis
from sqlalchemy.orm import declarative_base,sessionmaker
from database.config import settings

# mysql
DATABASE_URL = settings.mysql_url

# mongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
db_name = client['fast_api_mongo_db']

# redis
redis_db = redis.from_url(settings.redis_url)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
