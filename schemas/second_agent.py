from pydantic import BaseModel


class SecondAgentSchemas(BaseModel):
    memoria: bool
    corajoso: bool
    explorador: bool
    assassino: bool
    garimpeiro: bool
    forma_de_busca: int = 1
