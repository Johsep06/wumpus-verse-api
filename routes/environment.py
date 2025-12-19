from fastapi import APIRouter, Depends
from datetime import datetime
from sqlalchemy.orm import Session

from schemas import EnviromentSchemas, UserSchemas
from dependencies import get_session, check_token
from models import Environment, Room

environment_router = APIRouter(prefix='/environment', tags=['environment'])


@environment_router.get('/')
async def home():
    '''
    Rota padrão do ambiente
    '''

    return {"msg": "rota padrão do ambiente"}


@environment_router.post('/')
async def new_environment(
    environment_schemas: EnviromentSchemas, 
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

    objects_database_ids = {
        'W': 1,
        'P': 2,
        'O': 3,
    }

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
                objeto_id=objects_database_ids['P']
            )
            session.add(room_object)
        if sala.ouro:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=objects_database_ids['O']
            )
            session.add(room_object)
        if sala.wumpus:
            room_object = RoomObject(
                ambiente_id=environment_id,
                posicao_x=sala.x,
                posicao_y=sala.y,
                objeto_id=objects_database_ids['W']
            )
            session.add(room_object)

    session.commit()

    return {'msg': 'ambiente criado com sucesso'}
