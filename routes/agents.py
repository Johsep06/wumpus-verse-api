from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from schemas import UserSchemas, AgentSchemas, ThirdAgentSchemas, SecondAgentSchemas
from dependencies import get_session, check_token
from models import AgentDB, SecondAgentDB, ThirdAgentDB, \
    build_agent_record, build_agent_schemas, \
    build_second_agent_record, build_second_agent_schemas, \
    build_third_agent_record, build_third_agent_schemas
from src import validate_fitness

agents_router = APIRouter(prefix='/agents', tags=['agents'])


@agents_router.get('/')
async def home(
    page: int = 1,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    offset = (page - 1) * limit

    agents_list = session.query(AgentDB) \
        .order_by(desc(AgentDB.data)) \
        .all()

    if agents_list is None:
        return []

    agents: list[AgentSchemas] = []
    for i in range(offset, (offset + limit)):
        try:
            agent = agents_list[i]
        except IndexError:
            break

        agent_schemas = build_agent_schemas(agent)

        if agent_schemas.tipo == 2:
            second_agent = session.query(SecondAgentDB) \
                .filter(SecondAgentDB.id == agent.id) \
                .first()

            agent_schemas.properties = build_second_agent_schemas(second_agent)

        elif agent_schemas.tipo == 3:
            third_agent = session.query(ThirdAgentDB) \
                .filter(ThirdAgentDB.agent_id == agent.id) \
                .first()
            agent_schemas.properties = build_third_agent_schemas(third_agent)
        agents.append(agent_schemas)

    end_of_list = (offset + limit) >= len(agents_list)
    agents.append(end_of_list)

    return agents


@agents_router.post('/user')
async def new_agent(
    agent_type: int,
    name: str,
    second_agent_schemas: SecondAgentSchemas = None,
    third_agent_schemas: ThirdAgentSchemas = None,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    agent = build_agent_record(
        user_id=user_schemas.id,
        nome=name,
        data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tipo=agent_type,
    )

    session.add(agent)
    session.flush()

    if agent_type == 2:
        second_agent = build_second_agent_record(
            agent.id,
            second_agent_schemas,
        )

        session.add(second_agent)

    elif agent_type == 3:
        fitness_is_valid = validate_fitness(
            third_agent_schemas.fitness.replace(' ', '')
        )
        if not fitness_is_valid:
            raise HTTPException(
                status_code=400,
                detail='Função fitness inválida'
            )
        third_agent = build_third_agent_record(
            agent.id,
            third_agent_schemas
        )

        session.add(third_agent)

    session.commit()
    return {
        'status_code': 200,
        'detail': 'agente criado com sucesso'
    }


@agents_router.get('/user')
async def get_agent(
    agent_id: int,
    session: Session = Depends(get_session),
):
    agent_data = session.query(AgentDB) \
        .filter(AgentDB.id == agent_id) \
        .first()

    if agent_data is None:
        raise HTTPException(
            status_code=404,
            detail='Agente não encontrado'
        )

    agent = build_agent_schemas(agent_data)
    if agent_data.tipo == 2:
        properties = session.query(SecondAgentDB) \
            .filter(SecondAgentDB.id == agent_data.id)\
            .first()
        agent.properties = build_second_agent_schemas(properties)

    elif agent_data.tipo == 3:
        properties = session.query(ThirdAgentDB) \
            .filter(ThirdAgentDB.agent_id == agent_data.id)\
            .first()
        agent.properties = build_third_agent_schemas(properties)

    return agent


@agents_router.put('/user')
async def update_agent(
    agent_id: int,
    name: str,
    second_agent_schemas: SecondAgentSchemas = None,
    third_agent_schemas: ThirdAgentSchemas = None,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    agent = session.query(AgentDB) \
        .filter(AgentDB.id == agent_id) \
        .first()

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail='O agente não existe no banco de dados'
        )
    if user_schemas.id != agent.user_id:
        raise HTTPException(
            status_code=403,
            detail='O usuário não tem permisão para realizar essa ação'
        )

    agent.nome = name
    if agent.tipo == 2:
        properties = session.query(SecondAgentDB) \
            .filter(SecondAgentDB.id == agent_id) \
            .first()

        properties.coragem = second_agent_schemas.corajoso
        properties.explorador = second_agent_schemas.explorador
        properties.assassino = second_agent_schemas.cacador
        properties.busca_ouro = second_agent_schemas.garimpeiro
        properties.forma_de_busca = second_agent_schemas.forma_de_busca

    elif agent.tipo == 3:
        properties = session.query(ThirdAgentDB) \
            .filter(ThirdAgentDB.agent_id == agent_id) \
            .first()

        properties.populacao = third_agent_schemas.populacao
        properties.geracoes = third_agent_schemas.geracoes
        properties.taxa_de_cruzamento = third_agent_schemas.taxa_de_cruzamento
        properties.taxa_de_mutacao = third_agent_schemas.taxa_de_mutacao
        properties.fitness = third_agent_schemas.fitness

    session.commit()
    return {
        'status code': 200,
        'detail': 'Agente atualizado com sucesso'
    }


@agents_router.delete('/user')
async def delete_agent(
    agent_id: int,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):

    agent = session.query(AgentDB).filter(AgentDB.id == agent_id).first()

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail='O agente não existe no banco de dados'
        )
    if user_schemas.id != agent.user_id:
        raise HTTPException(
            status_code=403,
            detail='O usuário não tem permisão para realizar essa ação'
        )

    session.delete(agent)
    session.commit()
    return {
        'status_code': 200,
        'detail': 'Agente deletado com sucesso.',
    }


@agents_router.get('/agents')
async def list_agents(
    page: int = 1,
    limit: int = 5,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    offset = (page - 1) * limit

    agents_list = session.query(AgentDB) \
        .filter(AgentDB.user_id == user_schemas.id) \
        .order_by(desc(AgentDB.data)) \
        .all()

    if agents_list is None:
        return []

    agents: list[AgentSchemas] = []
    for i in range(offset, (offset + limit)):
        try:
            agent = agents_list[i]
        except IndexError:
            break

        agent_schemas = build_agent_schemas(agent)

        if agent_schemas.tipo == 2:
            second_agent = session.query(SecondAgentDB) \
                .filter(SecondAgentDB.id == agent.id) \
                .first()

            agent_schemas.properties = build_second_agent_schemas(second_agent)

        elif agent_schemas.tipo == 3:
            third_agent = session.query(ThirdAgentDB) \
                .filter(ThirdAgentDB.agent_id == agent.id) \
                .first()
            agent_schemas.properties = build_third_agent_schemas(third_agent)
        agents.append(agent_schemas)

    end_of_list = (offset + limit) >= len(agents_list)
    agents.append(end_of_list)

    return agents
