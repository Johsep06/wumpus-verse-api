from pydantic import BaseModel


class NumberEntitiesSchemas(BaseModel):
    wumpus: int
    buracos: int
    ouros: int
