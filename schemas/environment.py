from pydantic import BaseModel, field_serializer
from typing import List, Optional
from datetime import datetime

from .room import RoomSchemas
from .enviroments_statics import EnviromentsStaticsSchemas


class EnvironmentSchemas(BaseModel):
    id: Optional[int] = None
    nome: str
    largura: int
    altura: int
    data_criacao: Optional[datetime] = None
    estatisticas: EnviromentsStaticsSchemas
    salas: List[RoomSchemas]

    @field_serializer('data_criacao')
    def serialize_criado_em(self, dt: Optional[datetime], _info):
        # Verifica se dt não é None antes de formatar
        if dt is not None:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return None  # ou return dt (que seria None)
