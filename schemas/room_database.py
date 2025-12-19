from pydantic import BaseModel


class RoomDatabaseSchemas(BaseModel):
    ambiente_id: int
    posicao_x: int
    posicao_y: int
