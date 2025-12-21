from pydantic import BaseModel

from .enviroments_statics import EnviromentsStaticsSchemas


class EnvironmentResponseSchemas(BaseModel):
    id: int
    nome: str
    largura: int
    altura: int
    estatisticas: EnviromentsStaticsSchemas

    class Config:
        from_attributes = True
