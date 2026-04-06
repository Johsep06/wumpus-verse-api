from queue import PriorityQueue


def __h_score(start: tuple[int, int], stop: tuple[int, int]) -> int:
    distance_i = abs(start[0] - stop[0])
    distance_j = abs(start[1] - stop[1])

    return distance_i + distance_j


def __expand_positions(
    position: tuple[int, int],
    map_: dict[tuple[int, int], str],
    directions: dict[str, tuple[int, int]]
) -> list[tuple[int, int]]:
    neighbors = []

    for i, j in directions.values():
        neighbor = (position[0] + i, position[1] + j)
        if not neighbor in map_:
            continue

        neighbors.append((position[0] + i, position[1] + j))

    return neighbors


def __convert_into_directions(
    start: tuple[int, int],
    path: dict[tuple, tuple],
    directions: dict[tuple[int, int], str]
) -> list[str]:
    direction = []
    position = start
    for _ in range(len(path)):
        i = path[position][0] - position[0]
        j = path[position][1] - position[1]

        direction.append(str(directions[(i, j)]))
        position = path[position]

    return direction


def reverse_dict_directions(directions: dict[tuple[int, int], str]):
    new_directions: dict[str, tuple[int, int]] = {}
    for position in directions:
        new_directions.setdefault(directions[position], position)

    return new_directions


def a_star(
    start: tuple[int, int],
    stop: tuple[int, int],
    map_: dict[tuple[int, int], str],
    obstacles: list[str],
    directions: dict[tuple[int, int], str]
) -> list[str]:
    f_score = {cell: float('inf') for cell in list(map_.keys())}
    g_score: dict[tuple, int] = {}

    g_score[start] = 0
    f_score[start] = g_score[start] + __h_score(start, stop)

    queue = PriorityQueue()
    item = (f_score[start], __h_score(start, stop), start)
    queue.put(item)

    path = {}

    while not queue.empty():
        position = queue.get()[2]

        if position == stop:
            break

        for new_position in __expand_positions(position, map_, directions):
            free_position = True

            for obstacle in obstacles:
                if obstacle in map_[new_position]:
                    free_position = False
                    break
            if not free_position:
                continue

            new_g_score = g_score[position] + 1
            new_f_score = new_g_score + __h_score(new_position, stop)

            if new_f_score < f_score[new_position]:
                f_score[new_position] = new_f_score
                g_score[new_position] = new_g_score

                item = (new_f_score, __h_score(new_position, stop), new_position)
                queue.put(item)
                path[new_position] = position

    final_path = {}
    analyzed_position = stop

    while analyzed_position != start:
        final_path[path[analyzed_position]] = analyzed_position
        analyzed_position = path[analyzed_position]

    route = __convert_into_directions(start, final_path, reverse_dict_directions(directions))
    return route


if __name__ == '__main__':
    mapa = {
        (0, 0): ' ', (0, 1): ' ', (0, 2): ' ', (0, 3): ' ',
        (1, 0): 'P', (1, 1): 'P', (1, 2): 'P', (1, 3): ' ',
        (2, 0): ' ', (2, 1): ' ', (2, 2): 'W', (2, 3): ' ',
        (3, 0): 'O', (3, 1): ' ', (3, 2): ' ', (3, 3): ' ',
    }
    direcoes = {'N': (-1, 0), 'S': (1, 0), 'L': (0, 1), 'O': (0, -1),
                # 'NO':(-1, -1), 'NE':(-1, 1), 'SO':(1, -1), 'SE':(1, 1)
    }

    print(a_star((0, 0), (3, 0), mapa, ['P', 'W'], direcoes))
