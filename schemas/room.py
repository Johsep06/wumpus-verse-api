from pydantic import BaseModel
from typing import List


class RoomSchemas(BaseModel):
    x: int
    y: int
    entidade: List[str]

    class Config:
        from_attributes = True