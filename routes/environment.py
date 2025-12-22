from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, delete

from schemas import EnvironmentSchemas, UserSchemas, EnviromentsStaticsSchemas, NumberEntitiesSchemas, EntityDensitySchemas, EnvironmentResponseSchemas, RoomSchemas
from dependencies import get_session, check_token
from models import Environment, Room, RoomObject, User

environment_router = APIRouter(prefix='/environment', tags=['environment'])

OBJECTS_DATABASE_IDS = {
    'W': 1,
    'P': 2,
    'O': 3,
}


def get_number_entities(session: Session, environment_id: int) -> NumberEntitiesSchemas:
    number_of_wumpus = (
        session.query(func.count(RoomObject.ambiente_id))
        .filter(RoomObject.ambiente_id == environment_id)
        .filter(RoomObject.objeto_id == 1)
        .scalar() or 0
    )
    number_of_poco = (
        session.query(func.count(RoomObject.ambiente_id))
        .filter(RoomObject.ambiente_id == environment_id)
        .filter(RoomObject.objeto_id == 2)
        .scalar() or 0
    )
    number_of_gold = (
        session.query(func.count(RoomObject.ambiente_id))
        .filter(RoomObject.ambiente_id == environment_id)
        .filter(RoomObject.objeto_id == 3)
        .scalar() or 0
    )

    return NumberEntitiesSchemas(
        wumpus=number_of_wumpus,
        buracos=number_of_poco,
        ouros=number_of_gold
    )


def get_entity_desity(rooms:int, number_entities:NumberEntitiesSchemas) -> EntityDensitySchemas:
    wumpus_density = number_entities.wumpus / rooms
    poco_density = number_entities.buracos / rooms
    gold_density = number_entities.ouros / rooms
    
    return EntityDensitySchemas(
        wumpus=f'{wumpus_density:.2f}%',
        buracos=f'{poco_density:.2f}%',
        ouros=f'{gold_density:.2f}%',
    )


def get_environments_statics(
    session: Session,
    environment_id: int,
    environment_height: int,
    environment_width: int,
) -> EnviromentsStaticsSchemas:
    environment_area = environment_height * environment_width

    number_of_rooms = (
        session.query(func.count(Room.ambiente_id))
        .filter(Room.ambiente_id == environment_id)
        .scalar() or 0
    )
    
    number_of_entities = get_number_entities(session, environment_id)
    
    return EnviromentsStaticsSchemas(
        totalSalas=environment_area,
        salasAtivas=number_of_rooms,
        salasInativas=environment_area - number_of_rooms,
        quantidadeEntidades=number_of_entities,
        densidadeEntidades=get_entity_desity(number_of_rooms, number_of_entities)
    )


def get_environment_summary(session: Session, environment_id: int) -> EnvironmentResponseSchemas:
    environment = session.query(Environment).filter(Environment.id == environment_id).first()
    
    return EnvironmentResponseSchemas(
        id=environment.id,
        nome=environment.nome,
        largura=environment.largura,
        altura=environment.altura,
        estatisticas=get_environments_statics(
            session, 
            environment_id,
            environment.altura,
            environment.largura,
        ),
    )


def get_entities_in_environment(session: Session, environment_id:int, entity_symbol:str) -> list[tuple[int, int]]:
    coordinates = (
        session.query(RoomObject.posicao_x, RoomObject.posicao_y)
            .filter(RoomObject.ambiente_id == environment_id)
            .filter(RoomObject.objeto_id == OBJECTS_DATABASE_IDS.get(entity_symbol))
            .all()
    )
    
    return coordinates


def get_rooms(session: Session, environment_id:int) -> list[RoomSchemas]:
    rooms = session.query(Room).filter(Room.ambiente_id == environment_id).all()
    wumpus_coordinates = get_entities_in_environment(session, environment_id, 'W')
    hole_coordinates = get_entities_in_environment(session, environment_id, 'P')
    gold_coordinates = get_entities_in_environment(session, environment_id, 'O')
    
    room_list = []
    for room in rooms:
        room_list.append(
            RoomSchemas(
                x=room.posicao_x,
                y=room.posicao_y,
                wumpus=(room.posicao_x, room.posicao_y) in wumpus_coordinates,
                buraco=(room.posicao_x, room.posicao_y) in hole_coordinates,
                ouro=(room.posicao_x, room.posicao_y) in gold_coordinates,
            )
        )
    
    return room_list

@environment_router.get('/')
async def home():
    '''
    Rota padrão do ambiente
    '''

    return {"msg": "rota padrão do ambiente"}


@environment_router.get('/user')
async def environment_by_id(environment_id:int, session:Session=Depends(get_session)):
    '''
    Rota responsável por resgatar um ambuente pelo id
    
    Args:
        environment_id: int (ID do ambiente para resgate)

    Returns:
        EnvironmentSchemas: padrão de dados para o ambiente
    '''
    environment = session.query(Environment).filter(Environment.id == environment_id).first()
    environment_statics = get_environments_statics(
        session, 
        environment_id,
        environment.altura,
        environment.largura,
    )
    environment_rooms = get_rooms(session, environment_id)
    
    return EnvironmentSchemas(
        id=environment_id,
        nome=environment.nome,
        largura=environment.largura,
        altura=environment.altura,
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

    environment = Environment(
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
        room = Room(
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


@environment_router.delete('/user')
async def delete_environment(
    environment_id:int,
    user_schemas:UserSchemas = Depends(check_token),
    session:Session=Depends(get_session),
):
    '''
    rota para deletar um ambiente de um usuário
    
    Args:
        environment_id: int

    Returns:
        dict: mensagem de sucesso
    '''
    
    environment = session.query(Environment).filter(Environment.id == environment_id).first()
    if environment is None:
        raise HTTPException(status_code=404, detail="Ambiente não encontrado")
    if environment.usuario_id != user_schemas.id:
        raise HTTPException(status_code=403, detail="O usuário não tem permissão para realizar essa operação")
    
    session.execute(delete(RoomObject).where(RoomObject.ambiente_id == environment_id))
    session.execute(delete(Room).where(Room.ambiente_id == environment_id))
    session.delete(environment)
    session.commit()
    
    return {
        'msg':'ambiente deletado com sucesso'
    }
    

@environment_router.get('/list-user')
async def user_environments(
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    '''
    Rota responável por listar todos os ambientes de um usuário logado
    
    
    
    Args:

    Returns:
        list: lista de ambientes
    '''
    user = session.query(User.id).filter(User.email == user_schemas.email)
    
    ids_enviroments_list = session.query(Environment.id).filter(Environment.usuario_id == user).all()
    ids_enviroments = [id for (id,) in ids_enviroments_list]
    environments = []
    
    for id_ in ids_enviroments:
        environments.append(get_environment_summary(session, id_))
    
    return environments


@environment_router.get('/mini-map')
async def get_mini_mapa(environment_id:int, session:Session=Depends(get_session)) -> list[RoomSchemas]:
    environment_rooms = get_rooms(session, environment_id)
    
    return environment_rooms