from pydantic import BaseModel, field_serializer
from datetime import datetime

from .enviroments_statics import EnviromentsStaticsSchemas


class EnvironmentResponseSchemas(BaseModel):
    id: int
    nome: str
    largura: int
    altura: int
    data_criacao: datetime
    estatisticas: EnviromentsStaticsSchemas

    @field_serializer('data_criacao')
    def serialize_criado_em(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
