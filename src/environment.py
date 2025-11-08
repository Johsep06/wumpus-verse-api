from .room import Room


class Environment:
    def __init__(self):
        self.id = 0
        self.largura = 0
        self.altura = 0
        self.salas: dict[tuple[int], Room] = {}

    def reset(self):
        self.largura = 0
        self.altura = 0
        self.salas = {}
