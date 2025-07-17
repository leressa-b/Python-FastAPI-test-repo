from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BaseDBModel(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True