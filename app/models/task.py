from uuid import UUID
from pydantic import BaseModel, Field
from schemas.base_entity import Status, Priority
from typing import Optional

class TaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: Status = Field(default=Status.OPEN)
    priority: Priority = Field(default=Priority.MEDIUM)
    owner_id: UUID
    
class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: Status
    priority: Priority
    owner_id: UUID

    class Config:
        orm_mode = True