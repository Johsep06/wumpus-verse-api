from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ExecutionDBSchemas(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    agente_id: int
    ambiente_id: int
    posicao_x: int
    posicao_y: int
    qtd_ouro: int
    qtd_flechas: int
    qtd_wumpus: int
    pontos: int
    data: datetime
    qtd_passos:int
    historico: List[str]
