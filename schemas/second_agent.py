from pydantic import BaseModel


class SecondAgentSchemas(BaseModel):
    corajoso: bool
    explorador: bool
    cacador: bool
    garimpeiro: bool
    forma_de_busca: int = 1
