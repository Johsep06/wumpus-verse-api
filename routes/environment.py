from fastapi import APIRouter

from schemas import EnviromentSchemas, RoomSchemas
from src import Environment, Room

environment_router = APIRouter(prefix='/environment', tags=['environment'])


@environment_router.get('/')
async def home():
    '''
    Rota padrão do ambiente
    '''

    return {"msg": "rota padrão do ambiente"}


@environment_router.post('/')
async def new_environment(environment_schemas:EnviromentSchemas):
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
    enviroment = Environment()
    enviroment.altura = environment_schemas.altura
    enviroment.largura = environment_schemas.largura
    
    for sala in environment_schemas.salas:
        room = Room(sala.entidade)
        enviroment.salas[(sala.x, sala.y)] = room

    return {'msg':'ambiente criado com sucesso'}