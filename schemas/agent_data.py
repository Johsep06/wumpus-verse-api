from pydantic import BaseModel
from .second_agent import SecondAgentSchemas
from .third_agent import ThirdAgentSchemas


class AgentDataSchemas(BaseModel):
    id: int
    type: int = 0
    position_x: int
    position_y: int