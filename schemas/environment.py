from pydantic import BaseModel
from typing import List, Optional

from .room import RoomSchemas
from .enviroments_statics import EnviromentsStaticsSchemas


class EnvironmentSchemas(BaseModel):
    id: Optional[int]
    nome: str
    largura: int
    altura: int
    estatisticas: EnviromentsStaticsSchemas
    salas: List[RoomSchemas]

    class Config:
        from_attributes = True
