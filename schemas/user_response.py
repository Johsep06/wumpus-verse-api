from pydantic import BaseModel
from datetime import datetime


class UserResponseSchemas(BaseModel):
    email: str
    name: str
    created_at: datetime
