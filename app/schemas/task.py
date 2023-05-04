from sqlalchemy import Column, ForeignKey, String, Uuid, Enum
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity, Status, Priority

class Task(Base, BaseEntity):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(Enum(Status), default=Status.OPEN)
    priority = Column(Enum(Priority), default=Priority.LOW)
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    owners = relationship("User")