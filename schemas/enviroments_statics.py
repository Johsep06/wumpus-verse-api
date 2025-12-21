from pydantic import BaseModel

from .entity_density import EntityDensitySchemas
from .number_entities import NumberEntitiesSchemas


class EnviromentsStaticsSchemas(BaseModel):
    totalSalas: int
    salasAtivas: int
    salasInativas: int
    quantidadeEntidades: NumberEntitiesSchemas
    densidadeEntidades: EntityDensitySchemas
