from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ThirdAgentSchemas(BaseModel):
    populacao: int = Field(..., gt=0, description="Tamanho da população")
    geracoes: int = Field(..., gt=0, description="Número de gerações")
    taxa_de_cruzamento: float = Field(
        ..., 
        ge=1, 
        le=100,
        description="Taxa de cruzamento (1 a 100)"
    )
    taxa_de_mutacao: float = Field(
        ..., 
        ge=1, 
        le=100,
        description="Taxa de mutação (1 a 100)"
    )
    fitness: str
