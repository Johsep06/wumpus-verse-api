from pydantic import BaseModel


class TurnSchemas(BaseModel):
    agente: str
    posicao_x: int
    posicao_y: int
    acao: str
    ouros: int = 0
    flechas: int = 0
    pontos: int = 0
