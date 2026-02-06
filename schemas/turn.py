from pydantic import BaseModel


class TurnSchemas(BaseModel):
    agente: str
    posicao_x: int
    posicao_y: int
    acao: str
    tiro_position: tuple[int, int] = (0, 0)
    ouros: int = 0
    flechas: int = 0
    pontos: int = 0
