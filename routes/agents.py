from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from schemas import UserSchemas, AgentDBSchemas, ThirdAgentSchemas
from dependencies import get_session, check_token
from models import AgentDB, ThirdAgentDB

agents_router = APIRouter(prefix='/agents', tags=['agents'])


@agents_router.get('/')
async def home(
    page: int = 1,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    offset = (page - 1) * limit
    return


@agents_router.post('/user')
async def new_agent(
    agent_type: int,
    third_agent_schemas: ThirdAgentSchemas,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    agent = AgentDB(
        user_id=user_schemas.id,
        data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tipo=agent_type,
    )

    session.add(agent)
    session.flush()

    if agent_type == 3:
        third_agent = ThirdAgentDB(
            agent_id=agent.id,
            populacao=third_agent_schemas.populacao,
            geracoes=third_agent_schemas.geracoes,
            taxa_de_cruzamento=third_agent_schemas.taxa_de_cruzamento,
            taxa_de_mutacao=third_agent_schemas.taxa_de_mutacao,
            fitness=third_agent_schemas.fitness
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
    agent_data = session.query(AgentDB).filter(AgentDB.id == agent_id).first()

    if agent_data is None:
        return HTTPException(status_code=404, detail='Agente não encontrado')

    agent = AgentDBSchemas(
        agent_id=agent_data.id,
        user_id=agent_data.user_id,
        data=agent_data.data,
        tipo=agent_data.tipo
    )
    if agent_data.tipo == 3:
        properties = session.query(ThirdAgentDB).filter(
            ThirdAgentDB.agent_id == agent_data.id).first()
        agent.properties = ThirdAgentSchemas(
            populacao=properties.populacao,
            geracoes=properties.geracoes,
            taxa_de_cruzamento=properties.taxa_de_cruzamento,
            taxa_de_mutacao=properties.taxa_de_mutacao,
            fitness=properties.fitness,
        )

    return {
        'agent': agent,
    }


@agents_router.put('/user')
async def update_agent(
    agent_id: int,
    third_agent_schemas: ThirdAgentSchemas,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    agent = session.query(AgentDB).filter(AgentDB.id == agent_id).first()

    if agent is None:
        raise HTTPException(status_code=404, detail='O agente não existe no banco de dados')
    if user_schemas.id != agent.user_id:
        raise HTTPException(status_code=403, detail='O usuário não tem permisão para realizar essa ação')

    if agent.tipo == 3:
        properties = session.query(ThirdAgentDB).filter(ThirdAgentDB.agent_id == agent_id).first()

        properties.populacao = third_agent_schemas.populacao
        properties.geracoes = third_agent_schemas.geracoes
        properties.taxa_de_cruzamento = third_agent_schemas.taxa_de_cruzamento
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
        raise HTTPException(status_code=404, detail='O agente não existe no banco de dados')
    if user_schemas.id != agent.user_id:
        raise HTTPException(status_code=403, detail='O usuário não tem permisão para realizar essa ação')

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

    agents: list[AgentDBSchemas] = []
    for i in range(offset, (offset + limit)):
        try:
            agent = agents_list[i]
        except IndexError:
            break

        agent_data = AgentDBSchemas(
            agent_id=agent.id,
            user_id=agent.user_id,
            data=agent.data,
            tipo=agent.tipo
        )

        if agent.tipo == 3:
            third_agent = session.query(ThirdAgentDB) \
                .filter(ThirdAgentDB.agent_id == agent.id) \
                .first()
            agent_data.properties = ThirdAgentSchemas(
                populacao=third_agent.populacao,
                geracoes=third_agent.populacao,
                taxa_de_cruzamento=third_agent.taxa_de_cruzamento,
                taxa_de_mutacao=third_agent.taxa_de_mutacao,
                fitness=third_agent.fitness
            )
        agents.append(agent_data)

    end_of_list = (offset + limit) >= len(agents_list)
    agents.append(end_of_list)

    return agents
