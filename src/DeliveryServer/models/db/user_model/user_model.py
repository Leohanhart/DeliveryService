import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RoleEnum(enum.Enum):
    admin = "ADMIN"
    user = "USER"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum("USER", "ADMIN", name="role_enum") )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())