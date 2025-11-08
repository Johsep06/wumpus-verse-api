from pydantic import BaseModel
from typing import List

from .room import RoomSchemas


class EnviromentSchemas(BaseModel):
    largura: int
    altura:int
    salas: List[RoomSchemas]
    
    class Config:
        from_attributes = True
