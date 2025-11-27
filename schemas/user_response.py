from pydantic import BaseModel
from datetime import datetime


class UserResponseSchemas(BaseModel):
    uid: str
    email: str
    name: str
    created_at: datetime
