from pydantic import BaseModel


class RoomObjectDatabaseSchemas(BaseModel):
    ambiente_id: int
    posicao_x: int
    posicao_y: int
    objeto_id: int
