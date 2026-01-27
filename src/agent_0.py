from .agent import Agent
import random

class Agent0(Agent):
    def __init__(self, tag: str, position:tuple[int, int]):
        super().__init__(tag, position)
        self.type = 0

    def execute(self, data_position: dict):
        choice = random.choice(data_position['directions'])
        if 'br' in data_position['perception']:
            return 'x'

        return choice