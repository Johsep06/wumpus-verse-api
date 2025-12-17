from pydantic import BaseModel


class RoomSchemas(BaseModel):
    x: int
    y: int
    wumpus: bool
    buraco: bool
    ouro: bool

    class Config:
        from_attributes = True