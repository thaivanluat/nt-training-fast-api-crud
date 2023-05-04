from sqlalchemy import Boolean, Column, String, Uuid, ForeignKey
from database import Base
from schemas.base_entity import BaseEntity
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(Base, BaseEntity):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)

    tasks = relationship("Task", back_populates="owners")
    companies = relationship("Company")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)