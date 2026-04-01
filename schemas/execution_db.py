from pydantic import BaseModel
from typing import Optional, List


class ExecutionDBSchemas(BaseModel):
    id: Optional[int]
    agente_id: int
    ambiente_id: int
    posicao_x: int
    posicao_y: int
    qtd_ouro: int
    qtd_flechas: int
    qtd_wumpus: int
    pontos: int
    historico: List[str]
