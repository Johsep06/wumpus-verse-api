from datetime import datetime

from .engine import Base
from schemas import AgentSchemas, SecondAgentSchemas, ThirdAgentSchemas

AgentDB = Base.classes.primeiro_agente
SecondAgentDB = Base.classes.segundo_agente
ThirdAgentDB = Base.classes.terceiro_agente


def build_agent_record(user_id: int, nome: str, data: datetime, tipo: int):
    agent_db = AgentDB(
        user_id=user_id,
        nome=nome,
        data=data,
        tipo=tipo,
    )

    return agent_db


def build_agent_schemas(agent_db: AgentDB):
    agent_schemas = AgentSchemas(
        id=agent_db.id,
        user_id=agent_db.user_id,
        nome=agent_db.nome,
        data=agent_db.data,
        tipo=agent_db.tipo,
        properties=None,
    )

    return agent_schemas


def build_second_agent_record(agent_id: int, second_agent_schemas: SecondAgentSchemas):
    second_agent = SecondAgentDB(
        id=agent_id,
        coragem=second_agent_schemas.corajoso,
        explorador=second_agent_schemas.explorador,
        assassino=second_agent_schemas.cacador,
        busca_ouro=second_agent_schemas.garimpeiro,
        forma_de_busca=1
    )

    return second_agent


def build_second_agent_schemas(second_agent_db: SecondAgentDB):
    second_agent_schemas = SecondAgentSchemas(
        corajoso=second_agent_db.coragem,
        explorador=second_agent_db.explorador,
        cacador=second_agent_db.assassino,
        garimpeiro=second_agent_db.busca_ouro,
        forma_de_busca=second_agent_db.forma_de_busca,
    )

    return second_agent_schemas


def build_third_agent_record(agent_id: int, third_agent_schemas: ThirdAgentSchemas):
    third_agent = ThirdAgentDB(
        agent_id=agent_id,
        populacao=third_agent_schemas.populacao,
        geracoes=third_agent_schemas.geracoes,
        taxa_de_cruzamento=third_agent_schemas.taxa_de_cruzamento,
        taxa_de_mutacao=third_agent_schemas.taxa_de_mutacao,
        fitness=third_agent_schemas.fitness,
    )

    return third_agent


def build_third_agent_schemas(third_agent_db: ThirdAgentDB):
    third_agent_schemas = ThirdAgentSchemas(
        populacao=third_agent_db.populacao,
        geracoes=third_agent_db.geracoes,
        taxa_de_cruzamento=third_agent_db.taxa_de_cruzamento,
        taxa_de_mutacao=third_agent_db.taxa_de_mutacao,
        fitness=third_agent_db.fitness,
    )

    return third_agent_schemas
