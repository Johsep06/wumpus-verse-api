from .agent import Agent
from .memory import Memory
from .a_star import a_star
from .cell import Cell

from schemas import SecondAgentSchemas


class Agent2(Agent):
    def __init__(
        self,
        tag: str,
        position: tuple[int, int],
        directions: dict[str, tuple[int, int]],
        properties: SecondAgentSchemas,
    ):
        super().__init__(tag, position)
        self.type = 1
        self.memory = Memory(position, directions)
        self.properties = properties
        self.action_queue = []

    def cell_to_str(self):
        out: dict[tuple[int, int], str] = {}

        for position in self.memory.cells:
            if not self.memory.cells[position].suspects:
                out.setdefault(position, self.memory.cells[position].objetcs)
            else:
                out.setdefault(
                    position, {*self.memory.cells[position].objetcs, 'danger'})

        return out

    def inventory_status(self):
        if self.gold > 0 and self.kills > 0:
            return True
        if self.kills > 0 and not self.properties.garimpeiro:
            return True
        if self.gold > 0 and not self.properties.assassino:
            return True

        return False

    def memory_status(self):
        has_safe_room = self.memory.has_in_memory(self.position, Cell.UNKNOW, True)
        has_danger_room = self.memory.has_in_memory(self.position, Cell.UNKNOW, False)

        if not self.properties.explorador:
            return True
        if (not has_safe_room) and (not has_danger_room):
            return True
        if (not has_safe_room) and (not self.properties.corajoso):
            return True

        return False

    def update_memory(self, has_stink: bool, has_breeze:bool, has_shine:bool):
        if has_stink and has_breeze:
            self.memory.suspect_cells(self.position, 'w_h')
        elif has_stink:
            self.memory.suspect_cells(self.position, 'w')
        elif has_breeze:
            self.memory.suspect_cells(self.position, 'h')
        else:
            self.memory.secure_cells(self.position)

        if has_shine:
            self.memory.mark_memory(self.position, 'G')

    def calculate_secure_route(self, secure_position:tuple[int, int]):
        secure_pah = a_star(
            self.position,
            secure_position,
            self.cell_to_str(),
            [Cell.WUMPUS, Cell.HOLE, 'danger'],
            self.memory.directions
        )
        
        return secure_pah
    
    def calculate_danger_route(self, danger_position:tuple[int, int], shot:bool = False):
        danger_path = a_star(
            self.position,
            danger_position,
            self.cell_to_str(),
            [Cell.HOLE],
            self.memory.directions
        )

        if shot:
            danger_path.append(danger_path.pop().lower())

        if len(danger_path) > 1:
            danger_path.pop()

        return danger_path

    def calculate_gold_route(self, gold_position:tuple[int, int]):
        gold_path = a_star(
            self.position,
            gold_position,
            self.cell_to_str(),
            [Cell.WUMPUS, Cell.HOLE, 'danger'],
            self.memory.directions
        )

        gold_path.append('x')
        self.memory.cells[gold_position].objetcs.discard(Cell.GOLD)
        return gold_path

    def calculate_wumpus_route(self, wumpus_position:tuple[int, int]):
        print(self.memory.cells[wumpus_position])
        wumpus_path = a_star(
            self.position,
            wumpus_position,
            self.cell_to_str(),
            [Cell.HOLE, 'danger'],
            self.memory.directions
        )
        
        shot_direction = wumpus_path.pop()
        wumpus_path.append(shot_direction.lower())
        
        self.memory.cells[wumpus_position].objetcs.discard(Cell.WUMPUS)
        if not self.memory.cells[wumpus_position].objetcs:
            self.memory.cells[wumpus_position].add_object(Cell.KNOW)
            self.memory.cells[wumpus_position].is_safe = True

        return wumpus_path

    def execute(self, data_position: dict):
        self.memory.add_cells(self.position, data_position['directions'])
        has_stink = 'f' in data_position['perception']
        has_breeze = 'b' in data_position['perception']
        has_shine = 'br' in data_position['perception']

        self.update_memory(has_stink, has_breeze, has_shine)
        if not data_position['objects']:
            self.memory.mark_memory(self.position, 'K')
            self.memory.cells[self.position].is_safe = True

        if self.action_queue:
            return self.action_queue.pop(0)

        has_gold = self.memory.has_in_memory(self.position, Cell.GOLD, True)
        has_wumpus = self.memory.has_in_memory(self.position, Cell.WUMPUS, False)
        has_safe_room = self.memory.has_in_memory(self.position, Cell.UNKNOW, True)
        has_danger_room = self.memory.has_in_memory(self.position, Cell.UNKNOW, False)
        has_arrow = self.arrows > 0

        if self.memory_status() and self.inventory_status():
            exit_position = self.memory.search_position(self.position, Cell.EXIT)
            self.action_queue = self.calculate_secure_route(exit_position[1:])

        elif has_gold and \
            has_wumpus and \
            (self.properties.assassino == self.properties.garimpeiro):

            gold_position = self.memory.search_position(self.position, Cell.GOLD, True)
            wumpus_position = self.memory.search_position(self.position, Cell.WUMPUS)

            if gold_position[0] > wumpus_position[0]:
                self.action_queue = self.calculate_gold_route(gold_position[1:])
            elif (gold_position[0] < wumpus_position[0]) and has_arrow:
                self.action_queue = self.calculate_wumpus_route(wumpus_position[1:])
            elif has_arrow:
                self.action_queue = self.calculate_wumpus_route(wumpus_position[1:])
            else:
                self.action_queue = self.calculate_gold_route(gold_position[1:])

        elif has_wumpus and self.properties.assassino and has_arrow:
            wumpus_position = self.memory.search_position(self.position, Cell.WUMPUS)
            self.action_queue = self.calculate_wumpus_route(wumpus_position[1:])

        elif has_gold and self.properties.garimpeiro:
            gold_position = self.memory.search_position(self.position, Cell.GOLD, True)
            self.action_queue = self.calculate_gold_route(gold_position[1:])

        elif has_safe_room:
            safe_position = self.memory.search_position(self.position, Cell.UNKNOW, True)
            self.action_queue = self.calculate_secure_route(safe_position[1:])

        elif has_danger_room and self.properties.corajoso:
            shot = True
            danger_position = self.memory.search_suspect_position(
                self.position, 
                Cell.HOLE_AND_WUMPUS_SUSPECT
            )
            if danger_position is None:
                danger_position = self.memory.search_suspect_position(
                    self.position,
                    Cell.WUMPUS_SUSPECT
                )
            if danger_position is None:
                danger_position = self.memory.search_suspect_position(
                    self.position,
                    Cell.HOLE_SUSPECT
                )
                shot = False

            self.action_queue = self.calculate_danger_route(danger_position[1:], shot)
        else:
            random_position = self.memory.random_position(self.position)
            self.action_queue = self.calculate_secure_route(random_position[1:])

        return self.action_queue.pop(0)
