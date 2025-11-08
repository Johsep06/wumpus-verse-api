from pydantic import BaseModel
from typing import List


class RoomSchemas(BaseModel):
    posicao: List[int]
    objetos: List[str]
