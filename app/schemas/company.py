from database import Base
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity, Rating, Mode

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String)
    description = Column(String)
    mode = Column(Enum(Mode), default=Mode.ACTIVE)
    rating = Column(Enum(Rating), default=Rating.FIVE_STAR)

    users = relationship("User", back_populates="companies")