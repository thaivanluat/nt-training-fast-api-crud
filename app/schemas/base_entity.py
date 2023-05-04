from sqlalchemy import Column, Uuid, Time
import enum
import uuid

class Mode(enum.Enum):
    ACTIVE = 'ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'

class Rating(enum.Enum):
    ONE_STAR = 'ONE_STAR'
    TWO_STAR = 'TWO_STAR'
    THREE_STAR = 'THREE_STAR'
    FOUR_STAR = 'FOUR_STAR'
    FIVE_STAR = 'FIVE_STAR'

class Status(enum.Enum):
    DONE = 'DONE'
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'

class Priority(enum.Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)