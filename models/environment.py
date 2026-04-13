from .engine import Base
from schemas import NumberEntitiesSchemas, EntityDensitySchemas, EnviromentsStaticsSchemas, \
    EnvironmentResponseSchemas, RoomSchemas

EnvironmentDb = Base.classes.ambiente
RoomDb = Base.classes.sala
RoomObject = Base.classes.sala_objeto

OBJECTS_DATABASE_IDS = {
    'W': 1,
    'P': 2,
    'O': 3,
}

def get_number_entities(environment: EnvironmentDb) -> NumberEntitiesSchemas:
    return NumberEntitiesSchemas(
        wumpus=environment.wumpus,
        buracos=environment.poco,
        ouros=environment.ouro
    )


def get_entity_desity(rooms: int, number_entities: NumberEntitiesSchemas) -> EntityDensitySchemas:
    wumpus_density = number_entities.wumpus / rooms if rooms != 0 else 0
    poco_density = number_entities.buracos / rooms if rooms != 0 else 0
    gold_density = number_entities.ouros / rooms if rooms != 0 else 0

    return EntityDensitySchemas(
        wumpus=f'{wumpus_density:.2f}%',
        buracos=f'{poco_density:.2f}%',
        ouros=f'{gold_density:.2f}%',
    )


def get_environments_statics(environment: EnvironmentDb) -> EnviromentsStaticsSchemas:
    environment_area = environment.altura * environment.largura

    number_of_rooms = environment.salas_ativas
    number_of_entities = get_number_entities(environment)

    return EnviromentsStaticsSchemas(
        totalSalas=environment_area,
        salasAtivas=number_of_rooms,
        salasInativas=environment_area - number_of_rooms,
        quantidadeEntidades=number_of_entities,
        densidadeEntidades=get_entity_desity(number_of_rooms, number_of_entities)
    )


def get_environment_summary(environment: EnvironmentDb) -> EnvironmentResponseSchemas:
    return EnvironmentResponseSchemas(
        id=environment.id,
        nome=environment.nome,
        largura=environment.largura,
        altura=environment.altura,
        data_criacao=environment.data_criacao,
        estatisticas=get_environments_statics(environment)
    )


def get_entities_in_environment(entities_coordinates: tuple[int, int], entity_symbol: str) -> list[tuple[int, int]]:
    coordinates = list(
        filter(
            lambda c: c[2] == OBJECTS_DATABASE_IDS.get(entity_symbol),
            entities_coordinates
        )
    )
    coordinates = list(map(lambda c: (c.posicao_x, c.posicao_y), coordinates))

    return coordinates


def get_rooms(entities: tuple[int, int, int], rooms: RoomDb) -> list[RoomSchemas]:
    wumpus_coordinates = get_entities_in_environment(entities, 'W')
    hole_coordinates = get_entities_in_environment(entities, 'P')
    gold_coordinates = get_entities_in_environment(entities, 'O')

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
