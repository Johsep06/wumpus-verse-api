class Room:
    def __init__(self, entidade:list, *args, **kwargs):
        self.entidade = '' if entidade is None else entidade