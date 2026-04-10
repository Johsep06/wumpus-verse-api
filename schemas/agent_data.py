from pydantic import BaseModel
from .second_agent import SecondAgentSchemas
from .third_agent import ThirdAgentSchemas


class AgentDataSchemas(BaseModel):
    id: int
    type: int = 0
    position_x: int
    position_y: int
    second_agent_properties: SecondAgentSchemas
    third_agent_properties: ThirdAgentSchemas