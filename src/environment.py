from schemas import RoomSchemas

from .room import Room


class Environment:
    def __init__(
        self, id_: int, 
        height: int, 
        width:int, 
        diagonal_movement: bool, 
        rooms: list[RoomSchemas], 
        agents: dict[str, tuple[int, int]]
):

        self.id = id_
        self.height = height
        self.width = width
        self.rooms: dict[tuple[int, int], Room] = {}
        self.entities_positions = {'W': [], 'P': [], 'O': []}
        self.directions = {'N':(-1, 0), 'S':(1, 0), 'L':(0, 1), 'O':(0, -1)}
        self.agents = agents
        
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
                    line.append(f'{','.join(self.rooms[(x, y)].perceptions): ^7}')
            screen.append('|'.join(line))
        
        return '\n'.join(screen)
        
    
    def display_agents(self) -> str:
        display = ['--- Agentes ---']
        
        for agent in self.agents:
            display.append(f'{agent} | x:{self.agents[agent][0]}, y:{self.agents[agent][1]}')
        
        display.append('---------------')
        
        return '\n'.join(display)
            
    def reset(self):
        self.rooms = {}

    def set_perceptions(self, perception:str, position:tuple[int, int]):
        if position not in self.rooms:
            return
        
        for x, y in list(self.directions.values()):
            if (position[0] + x, position[1] + y) not in self.rooms:
                continue
            self.rooms[(position[0] + x, position[1] + y)].add_perception(perception)
    
    def get_directions(self, agent_id:str) -> list[str]:
        pos_x, pos_y = self.agents[agent_id]
        directions = []
        
        for key in self.directions:
            if (pos_x + self.directions[key][0], pos_y + self.directions[key][1]) in self.rooms:
                directions.append(key)
                
        return directions
    
    def move_agent(self, agent_id:str, direction:str):
        if direction not in self.directions:
            return
        
        direction_tuple = self.directions[direction]
        agent_position = self.agents[agent_id]
        new_agent_position = (
            agent_position[0] + direction_tuple[0], 
            agent_position[1] + direction_tuple[1]
        )
        
        if new_agent_position not in self.rooms:
            return
        
        self.agents[agent_id] = new_agent_position
        
        return ','.join(self.rooms[new_agent_position].entities)