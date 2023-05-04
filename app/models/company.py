from pydantic import BaseModel, Field, root_validator
from uuid import UUID
from schemas.base_entity import Mode, Rating
from typing import Optional
from datetime import datetime

class CompanyModel(BaseModel):
    name: Optional[str] = Field(min_length=3) 
    description: Optional[str] = Field(min_length=5)
    mode: Mode = Field(default=Mode.ACTIVE)
    rating: Rating = Field(default=Rating.FIVE_STAR)

class CompanyViewModel(BaseModel):
    id: UUID 
    name: str
    description: str
    mode: Mode
    rating: Rating
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True