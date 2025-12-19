from pydantic import BaseModel
from typing import List

from .room import RoomSchemas
from .enviroments_statics import EnviromentsStaticsSchemas


class EnviromentSchemas(BaseModel):
    nome: str
    largura: int
    altura: int
    estatisticas: EnviromentsStaticsSchemas
    salas: List[RoomSchemas]

    class Config:
        from_attributes = True
