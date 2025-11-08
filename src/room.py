class Room:
    def __init__(self, entidade:list, percepcao:list, *args, **kwargs):
        self.entidade = '' if entidade is None else entidade
        self.percepcao = '' if percepcao is None else percepcao