from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .third_agent import ThirdAgentSchemas


class AgentDBSchemas(BaseModel):
    agent_id: Optional[int]
    user_id: int
    data: datetime
    tipo: int
    properties: ThirdAgentSchemas | None = None
