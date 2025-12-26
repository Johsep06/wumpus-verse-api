from pydantic import BaseModel, field_serializer
from typing import List, Optional
from datetime import datetime

from .room import RoomSchemas
from .enviroments_statics import EnviromentsStaticsSchemas


class EnvironmentSchemas(BaseModel):
    id: Optional[int]
    nome: str
    largura: int
    altura: int
    data_criacao: Optional[datetime]
    estatisticas: EnviromentsStaticsSchemas
    salas: List[RoomSchemas]

    @field_serializer('data_criacao')
    def serialize_criado_em(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
