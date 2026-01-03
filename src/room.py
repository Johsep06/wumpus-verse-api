class Room:
    def __init__(self, entity: list, *args, **kwargs):
        self.entities: list[str] = [] if entity is None else entity
        self.perceptions: list[str] = []

    def add_perception(self, perception: str):
        if perception not in self.perceptions:
            perception.append(perception)

    def hide_perception(self, perception: str):
        if perception in self.perceptions:
            index = self.perceptions.index(perception)
            self.perceptions[index] = perception.upper()

    def reveal_perception(self, perception: str):
        if perception in self.perceptions:
            index = self.perceptions.index(perception)
            self.perceptions[index] = perception.lower()

    def add_entity(self, entity:str):
        self.entities.append(entity)

    def hide_entity(self, entity:str):
        if entity in self.entities:
            index = self.entities.index(entity)
            self.entities[index] = entity.lower()
    
    def reveal_entity(self, entity:str):
        if entity in self.entities:
            index = self.entities.index(entity)
            self.entities[index] = entity.upper()