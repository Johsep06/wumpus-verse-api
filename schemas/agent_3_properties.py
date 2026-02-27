from pydantic import BaseModel, Field


class Agent3PropertiesSchemas(BaseModel):
    populacao: int = Field(..., gt=0, description="Tamanho da população")
    geracoes: int = Field(..., gt=0, description="Número de gerações")
    taxa_de_cruzamento: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Taxa de cruzamento (0.0 a 1.0)"
    )
    taxa_de_mutacao: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Taxa de mutação (0.0 a 1.0)"
    )
