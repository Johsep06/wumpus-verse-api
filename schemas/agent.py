from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

from .second_agent import SecondAgentSchemas
from .third_agent import ThirdAgentSchemas


class AgentSchemas(BaseModel):
    id: Optional[int] = None
    user_id: int
    nome: Optional[str]
    data: Optional[datetime] = None
    tipo: int
    properties: Optional[Union[SecondAgentSchemas, ThirdAgentSchemas]] = None
