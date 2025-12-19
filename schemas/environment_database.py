from pydantic import BaseModel


class EnvironmentDatabaseSchemas(BaseModel):
    nome: str
    largura: int
    altura: int
    data_criacao: str
