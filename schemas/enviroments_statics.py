from pydantic import BaseModel
from typing import List

from .entity_density import EntityDensitySchemas
from .number_entities import NumberEntitiesSchemas
from .room import RoomSchemas


class EnviromentsStaticsSchemas(BaseModel):
    totalSalas: int
    salasAtivas: int
    salasInativas: int
    quantidadeEntidades: NumberEntitiesSchemas
    densidadeEntidades: EntityDensitySchemas
