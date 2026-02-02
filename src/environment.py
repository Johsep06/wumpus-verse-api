from schemas import RoomSchemas, TurnSchemas

from .room import Room
from .agent import Agent


class Environment:
    def __init__(
        self, id_: int,
        diagonal_movement: bool,
        rooms: list[RoomSchemas],
    ):

        self.id = id_
        self.rooms: dict[tuple[int, int], Room] = {}
        self.entities_positions = {'W': [], 'P': [], 'O': []}
        self.directions = {'N': (-1, 0), 'S': (1, 0),
                           'L': (0, 1), 'O': (0, -1)}
        self.step_histor: list[TurnSchemas] = []
        self.agent_queue: list[Agent] = []

        if diagonal_movement:
            self.directions.setdefault('NO', (-1, -1))
            self.directions.setdefault('NE', (-1, 1))
            self.directions.setdefault('SO', (1, -1))
            self.directions.setdefault('SE', (1, 1))

        for room in rooms:
            self.rooms[room.x, room.y] = Room()
            if room.wumpus:
                self.rooms[room.x, room.y].add_entity('W')
                self.entities_positions['W'].append((room.x, room.y))

            if room.buraco:
                self.rooms[room.x, room.y].add_entity('P')
                self.entities_positions['P'].append((room.x, room.y))

            if room.ouro:
                self.rooms[room.x, room.y].add_entity('O')
                self.entities_positions['O'].append((room.x, room.y))
                self.rooms[room.x, room.y].add_perception('br')

        for position in self.entities_positions['W']:
            self.set_perceptions('f', position)

        for position in self.entities_positions['P']:
            self.set_perceptions('b', position)

    def set_data_for_display(self, height: int, width: int,):
        self.height = height
        self.width = width

    def display_entities(self) -> str:
        screen = []

        for x in range(self.width):
            line = []
            for y in range(self.height):
                if (x, y) not in self.rooms:
                    line.append('#'*7)
                else:
                    line.append(f'{','.join(self.rooms[(x, y)].entities): ^7}')
            screen.append('|'.join(line))

        return '\n'.join(screen)

    def display_perceptions(self) -> str:
        screen = []

        for x in range(self.width):
            line = []
            for y in range(self.height):
                if (x, y) not in self.rooms:
                    line.append('#######')
                else:
                    line.append(
                        f'{','.join(self.rooms[(x, y)].perceptions): ^7}')
            screen.append('|'.join(line))

        return '\n'.join(screen)

    def display_agents(self) -> str:
        display = ['--- Agentes ---']

        for agent in self.agent_queue:
            display.append(
                f'{agent.tag} | x:{agent.position[0]}, y:{agent.position[1]}')

        display.append('---------------')

        return '\n'.join(display)

    def add_agent(self, agent: Agent):
        self.agent_queue.append(agent)

    def set_perceptions(self, perception: str, position: tuple[int, int]):
        if position not in self.rooms:
            return

        for x, y in list(self.directions.values()):
            if (position[0] + x, position[1] + y) not in self.rooms:
                continue
            self.rooms[(position[0] + x, position[1] + y)
                       ].add_perception(perception)

    def get_directions(self, agent: Agent) -> list[str]:
        pos_x, pos_y = agent.position
        directions = []

        for key in self.directions:
            if (pos_x + self.directions[key][0], pos_y + self.directions[key][1]) in self.rooms:
                directions.append(key)

        return directions

    def move_agent(self, agent: Agent, direction: str):
        if direction not in self.directions:
            return

        direction_tuple = self.directions[direction]
        agent_position = agent.position
        new_agent_position = (
            agent_position[0] + direction_tuple[0],
            agent_position[1] + direction_tuple[1]
        )

        if new_agent_position not in self.rooms:
            return

        agent.position = new_agent_position

        return ','.join(self.rooms[new_agent_position].entities)

    def get_perception(self, agent: Agent):
        # agent_position = self.agents[agent_id]

        return self.rooms[agent.position].perceptions

    def get_agent_position_data(self, agent: Agent):
        agent_position_perception = self.get_perception(agent)
        agent_position_directions = self.get_directions(agent)

        return {
            'position': agent.position,
            'perception': agent_position_perception,
            'directions': agent_position_directions,
        }

    def agent_action(self, agent: Agent, action: str):
        position = agent.position
        result = None

        if action == 'x':
            if 'O' in self.rooms[agent.position].entities:
                self.rooms[agent.position].hide_entity('O')
                self.rooms[agent.position].hide_perception('br')
                result = 'O'
        elif action in self.directions:
            result = self.move_agent(agent, action)

        if result is None:
            return ''

        # self.step_histor.append(TurnSchemas(
        #     agente=agent.tag,
        #     posicao_x=position[0],
        #     posicao_y=position[1],
        #     acao=action,
        # ))

        return result

    def execution(self) -> list[TurnSchemas]:
        step_histor: list[TurnSchemas] = []
        # step_histor.append(TurnSchemas(
        #         agente=agent.tag,
        #         posicao_x=agent.position[0],
        #         posicao_y=agent.position[1],
        #         acao='',
        #         pontos=agent.pts,
        #     ))

        for agent in self.agent_queue:
            step_histor.append(TurnSchemas(
                agente=agent,
                posicao_x=agent.position[0],
                posicao_y=agent.position[1],
                acao='',
                pontos=0
            ))

        while True:
        # for _ in range(10):
            for agent in self.agent_queue:
                position_data = self.get_agent_position_data(agent)
                choice = agent.execute(position_data)
                agent_status = self.agent_action(agent, choice)
                if agent_status == 'O':
                    agent.gold += 1
                print(agent_status)
                agent.status = agent_status
                agent.update_pts()
                
                step_histor.append(TurnSchemas(
                    agente=agent.tag,
                    posicao_x=agent.position[0],
                    posicao_y=agent.position[1],
                    acao=choice,
                    pontos=agent.pts,
                ))
                if agent.game_over:
                    self.agent_queue.remove(agent)
                print(agent.position, agent.game_over, agent.gold)
            if self.agent_queue == []: break
        
        return step_histor
