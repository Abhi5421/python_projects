from sqlalchemy import Column,Integer,String,Boolean,VARCHAR
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(256), primary_key=True)
    email = Column(VARCHAR(256), unique=True, index=True)
    mobile = Column(Integer, unique=True, index=True)
    # hashed_password = Column(String)
    is_active = Column(Boolean, default=True)