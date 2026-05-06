import random

from .cell import Cell


class Memory:
    def __init__(self, start_position: tuple[int, int], directions: dict[str, tuple[int, int]]):
        position = Cell(object_=Cell.EXIT)
        position.is_safe = True
        self.cells: dict[tuple[int, int], Cell] = {
            start_position: position
        }
        self.directions = directions

    def expand_cells(self, position: tuple[int, int], directions: list[str] = None):
        if directions is None:
            directions = self.directions

        positions = []
        for direction in directions:
            new_position = (
                position[0] + self.directions[direction][0],
                position[1] + self.directions[direction][1],
            )

            positions.append(new_position)

        return positions

    def add_cells(self, position: tuple[int, int], directions: list[str]):
        positions = self.expand_cells(position, directions)

        for pos in positions:
            if pos in self.cells:
                continue
            self.cells.setdefault(pos, Cell())

    def mark_memory(self, position: tuple[int, int], symbol: str):
        marks = {
            'W': Cell.WUMPUS,
            'H': Cell.HOLE,
            'G': Cell.GOLD,
            'K': Cell.KNOW,
            'w': Cell.WUMPUS_SUSPECT,
            'h': Cell.HOLE_SUSPECT,
            'h_w': Cell.HOLE_AND_WUMPUS_SUSPECT,
            'w_h': Cell.HOLE_AND_WUMPUS_SUSPECT,

        }

        if (symbol == 'W_H') or (symbol == 'H_W'):
            self.cells[position].add_object(marks.setdefault('W'))
            self.cells[position].add_object(marks.setdefault('H'))
        elif symbol.isupper():
            self.cells[position].add_object(marks.setdefault(symbol))
        else:
            self.cells[position].add_suspect(marks.setdefault(symbol))

    def suspect_cells(self, position: tuple[int, int], symbol: str):
        suspects = []
        for direction in self.directions:
            suspect_cell = (
                position[0] + self.directions[direction][0],
                position[1] + self.directions[direction][1],
            )

            if suspect_cell not in self.cells:
                continue

            if self.cells[suspect_cell].is_safe:
                continue

            suspects.append(suspect_cell)

        if len(suspects) == 0:
            return
        elif len(suspects) == 1:
            self.mark_memory(suspects[0], symbol.upper())
        else:
            for pos in suspects:
                self.mark_memory(pos, symbol.lower())

    def secure_cells(self, position: tuple[int, int]):
        for direction in self.directions:
            secure_cell = (
                position[0] + self.directions[direction][0],
                position[1] + self.directions[direction][1],
            )

            if secure_cell not in self.cells:
                continue

            self.cells[secure_cell].is_safe = True

    def search_position(
        self,
        position: tuple[int, int],
        symbol: str,
        is_safe: bool = False
    ) -> tuple[int, int, int] | None:

        positions: list[tuple[int, int, int]] = []

        for cell in self.cells:
            if cell == position:
                continue
            if is_safe and (not self.cells[cell].is_safe):
                continue

            if symbol in self.cells[cell].objetcs:
                distance_i = abs(position[0] - cell[0])
                distance_j = abs(position[1] - cell[1])

                positions.append((
                    distance_i + distance_j,
                    cell[0],
                    cell[1]
                ))

        positions.sort()

        if not positions:
            return None

        return positions[0]

    def search_suspect_position(
        self,
        position: tuple[int, int],
        suspect: str,
    ) -> tuple[int, int, int] | None:

        positions: list[tuple[int, int, int]] = []

        for cell in self.cells:
            if cell == position:
                continue
            if self.cells[cell].is_safe:
                continue

            is_suspect = suspect in self.cells[cell].suspects
            is_unknow = Cell.UNKNOW in self.cells[cell].objetcs

            if is_suspect and is_unknow:
                distance_i = abs(position[0] - cell[0])
                distance_j = abs(position[1] - cell[1])

                positions.append((
                    distance_i + distance_j,
                    cell[0],
                    cell[1]
                ))

        positions.sort()

        if not positions:
            return None

        return positions[0]

    def random_position(self, start_position: tuple[int, int]):
        position = random.choice(list(self.cells.keys()))

        while position == start_position:
            position = random.choice(list(self.cells.keys()))

        return position

    def has_in_memory(self, start_position: tuple[int, int], value: str, is_safe: bool):
        for position in self.cells:
            if position == start_position:
                continue
            if self.cells[position].is_safe != is_safe:
                continue
            if value not in self.cells[position].objetcs:
                continue

            return True
        return False
