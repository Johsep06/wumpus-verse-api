from pydantic import BaseModel


class AgentDataSchemas(BaseModel):
    id: int
    type: int = 0
    position_x: int
    position_y: int
