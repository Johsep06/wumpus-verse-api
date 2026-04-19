from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import delete, desc

from schemas import EnvironmentSchemas, UserSchemas, RoomSchemas, \
    AgentDataSchemas, TurnSchemas
from dependencies import get_session, check_token
from models import EnvironmentDb, RoomDb, RoomObject, User, \
    AgentDB, SecondAgentDB, ThirdAgentDB, \
    build_agent_schemas, build_second_agent_schemas, build_third_agent_schemas, \
    get_rooms, get_environment_summary, get_environments_statics
from src import Environment, Agent, Agent1, Agent2, Agent3

environment_router = APIRouter(prefix='/environment', tags=['environment'])

OBJECTS_DATABASE_IDS = {
    'W': 1,
    'P': 2,
    'O': 3,
}


@environment_router.get('/')
async def home(
    page: int = 1,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    '''
    Rota responsável por listar o resumo de todos os ambientes no banco de dados.

    Args:
        page: int = 1 (página a ser exibida).
        limit: int = 5 (limite de itens por página).

    return:
        list: lista de ambientes
    '''

    offset = (page - 1) * limit

    ids_enviroments_list = session.query(EnvironmentDb.id) \
        .order_by(desc(EnvironmentDb.data_criacao)) \
        .all()
    ids_enviroments_list = [id for (id,) in ids_enviroments_list]
    ids_enviroments = ids_enviroments_list[offset:(offset + limit)]
    environments = []

    for id_ in ids_enviroments:
        environment = session.query(EnvironmentDb) \
            .filter(EnvironmentDb.id == id_) \
            .first()
        environments.append(get_environment_summary(environment))

    end_of_list = (offset + limit) >= len(ids_enviroments_list)
    environments.append(end_of_list)
    return environments


@environment_router.get('/user')
async def environment_by_id(environment_id: int, session: Session = Depends(get_session)):
    '''
    Rota responsável por resgatar um ambiente pelo id

    Args:
        environment_id: int (ID do ambiente para resgate)

    Returns:
        EnvironmentSchemas: padrão de dados para o ambiente
    '''
    environment = session.query(EnvironmentDb) \
        .filter(EnvironmentDb.id == environment_id) \
        .first()

    if environment is None:
        raise HTTPException(status_code=404, detail='Ambiente não encontrado')

    environment_statics = get_environments_statics(
        environment,
    )
    entities = session.query(RoomObject.posicao_x, RoomObject.posicao_y, RoomObject.objeto_id) \
        .filter(RoomObject.ambiente_id == environment_id) \
        .all()
    rooms = session.query(RoomDb) \
        .filter(RoomDb.ambiente_id == environment_id) \
        .all()
    environment_rooms = get_rooms(entities, rooms)

    return EnvironmentSchemas(
        id=environment_id,
        nome=environment.nome,
        largura=environment.largura,
        altura=environment.altura,
        data_criacao=environment.data_criacao,
        estatisticas=environment_statics,
        salas=environment_rooms,
    )


@environment_router.post('/user')
async def new_environment(
    environment_schemas: EnvironmentSchemas,
    session: Session = Depends(get_session),
    user: UserSchemas = Depends(check_token)
):
    """
    Cria um novo ambiente no sistema
    Args:
        environment_schemas (UsuarioSchemas) : padrão com os dados do ambiente
            largura: int
            altura: int
            salas: lista com os dados da sala (x:int, y:int, entidade:list[str])

    Returns:
        dict: mensagem de sucesso.
    """

    environment = EnvironmentDb(
        nome=environment_schemas.nome,
        largura=environment_schemas.largura,
        altura=environment_schemas.altura,
        data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        usuario_id=user.id
    )
    session.add(environment)
    session.flush()

    environment_id = environment.id

    for sala in environment_schemas.salas:
        room = RoomDb(
            ambiente_id=environment_id,
            posicao_x=sala.x,
            posicao_y=sala.y,
        )
        session.add(room)

        if sala.buraco:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=OBJECTS_DATABASE_IDS['P']
            )
            session.add(room_object)
        if sala.ouro:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=OBJECTS_DATABASE_IDS['O']
            )
            session.add(room_object)
        if sala.wumpus:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=OBJECTS_DATABASE_IDS['W']
            )
            session.add(room_object)

    session.commit()

    return {'msg': 'ambiente criado com sucesso'}


@environment_router.put('/user')
async def update_environment(
    environment_id: int,
    updated_environment: EnvironmentSchemas,
    user_schemas: UserSchemas = Depends(check_token),
    session: Session = Depends(get_session),
):
    environment = session.query(EnvironmentDb) \
        .filter(EnvironmentDb.id == environment_id) \
        .first()
    if environment is None:
        raise HTTPException(status_code=404, detail="Ambiente não encontrado")
    if environment.usuario_id != user_schemas.id:
        raise HTTPException(
            status_code=403,
            detail="O usuário não tem permissão para realizar essa operação"
        )

    session.execute(
        delete(RoomObject)
        .where(RoomObject.ambiente_id == environment_id)
    )
    session.execute(
        delete(RoomDb)
        .where(RoomDb.ambiente_id == environment_id)
    )

    environment.nome = updated_environment.nome
    environment.largura = updated_environment.largura
    environment.altura = updated_environment.altura

    for sala in updated_environment.salas:
        room = RoomDb(
            ambiente_id=environment_id,
            posicao_x=sala.x,
            posicao_y=sala.y,
        )
        session.add(room)

        if sala.buraco:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=OBJECTS_DATABASE_IDS['P']
            )
            session.add(room_object)
        if sala.ouro:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=OBJECTS_DATABASE_IDS['O']
            )
            session.add(room_object)
        if sala.wumpus:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=OBJECTS_DATABASE_IDS['W']
            )
            session.add(room_object)

    session.commit()

    return {'msg': 'ambiente atualizado com sucesso'}


@environment_router.delete('/user')
async def delete_environment(
    environment_id: int,
    user_schemas: UserSchemas = Depends(check_token),
    session: Session = Depends(get_session),
):
    '''
    rota para deletar um ambiente de um usuário

    Args:
        environment_id: int

    Returns:
        dict: mensagem de sucesso
    '''

    environment = session.query(EnvironmentDb) \
        .filter(EnvironmentDb.id == environment_id) \
        .first()
    if environment is None:
        raise HTTPException(status_code=404, detail="Ambiente não encontrado")
    if environment.usuario_id != user_schemas.id:
        raise HTTPException(
            status_code=403,
            detail="O usuário não tem permissão para realizar essa operação",
        )

    session.delete(environment)
    session.commit()

    return {'msg': 'ambiente deletado com sucesso'}


@environment_router.get('/list-user')
async def user_environments(
    page: int = 1,
    limit: int = 5,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    '''
    Rota responável por listar todos os ambientes de um usuário logado

    Args:

    Returns:
        list: lista de ambientes
    '''
    offset = (page - 1) * limit

    ids_enviroments_list = session.query(EnvironmentDb.id) \
        .filter(EnvironmentDb.usuario_id == user_schemas.id) \
        .order_by(desc(EnvironmentDb.data_criacao)) \
        .all()
    ids_enviroments_list = [id for (id,) in ids_enviroments_list]
    ids_enviroments = ids_enviroments_list[offset:(offset + limit)]
    environments = []

    for id_ in ids_enviroments:
        environment = session.query(EnvironmentDb).filter(
            EnvironmentDb.id == id_).first()
        environments.append(get_environment_summary(environment))

    end_of_list = (offset + limit) >= len(ids_enviroments_list)
    environments.append(end_of_list)
    return environments


@environment_router.get('/mini-map')
async def get_mini_mapa(environment_id: int, session: Session = Depends(get_session)) -> list[RoomSchemas]:
    environment = session.query(EnvironmentDb) \
        .filter(EnvironmentDb.id == environment_id) \
        .first()
    if environment is None:
        raise HTTPException(status_code=404, detail='Ambiente não encontrado')

    entities = session.query(RoomObject.posicao_x, RoomObject.posicao_y, RoomObject.objeto_id) \
        .filter(RoomObject.ambiente_id == environment_id) \
        .all()
    rooms = session.query(RoomDb) \
        .filter(RoomDb.ambiente_id == environment_id) \
        .all()
    environment_rooms = get_rooms(entities, rooms)

    return environment_rooms


@environment_router.post('/execution')
async def execution(
    environment_id: int,
    diagonal_movement: bool,
    agents_data: list[AgentDataSchemas],
    session: Session = Depends(get_session)
) -> list[TurnSchemas]:
    entities = session.query(RoomObject.posicao_x, RoomObject.posicao_y, RoomObject.objeto_id) \
        .filter(RoomObject.ambiente_id == environment_id) \
        .all()
    rooms_db = session.query(RoomDb) \
        .filter(RoomDb.ambiente_id == environment_id) \
        .all()
    rooms = get_rooms(entities, rooms_db)
    enviroment = Environment(
        id_=environment_id,
        diagonal_movement=diagonal_movement,
        rooms=rooms
    )

    for data in agents_data:
        agent: Agent = None

        agent_db = session.query(AgentDB) \
            .filter(AgentDB.id == data.id) \
            .first()

        if not agent_db:
            raise HTTPException(
                status_code=404,
                detail='Agente não encontrado',
            )

        if agent_db.tipo == 1:
            agent = Agent1(data.id, (data.position_y, data.position_x))
        elif agent_db.tipo == 2:
            second_agent_data = session.query(SecondAgentDB) \
                .filter(SecondAgentDB.id == agent_db.id) \
                .first()

            second_agent = build_second_agent_schemas(
                second_agent_data
            )
            agent = Agent2(
                data.id,
                (data.position_y, data.position_x),
                enviroment.directions,
                second_agent
            )
        elif agent_db.tipo == 3:
            third_agent_data = session.query(ThirdAgentDB) \
                .filter(ThirdAgentDB.agent_id == agent_db.id) \
                .first()

            third_agent = build_third_agent_schemas(
                third_agent_data
            )
            agent = Agent3(
                data.id,
                (data.position_y, data.position_x),
                enviroment.directions,
                enviroment.get_map(),
                third_agent,
            )

        enviroment.add_agent(agent)

    step_histor = enviroment.execution()

    return step_histor
