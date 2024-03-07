from sqlalchemy import Column, Integer, Boolean, VARCHAR,DateTime
from database.connection import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(VARCHAR(256),nullable=True)
    email = Column(VARCHAR(256), unique=True, index=True)
    mobile = Column(VARCHAR(20), unique=True, index=True,nullable=True)
    password = Column(VARCHAR(256),unique=True)
    is_active = Column(Boolean, default=True,nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow(), onupdate=datetime.utcnow())

    def user_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

