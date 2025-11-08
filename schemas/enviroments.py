from pydantic import BaseModel
from typing import List

from .room import RoomSchemas


class EnviromentSchemas(BaseModel):
    quantidade_salas: int
    salas: List[RoomSchemas]
