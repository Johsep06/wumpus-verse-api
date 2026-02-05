from .agent import Agent
import random

class Agent0(Agent):
    def __init__(self, tag: str, position:tuple[int, int]):
        super().__init__(tag, position)
        self.type = 0

    def execute(self, data_position: dict) -> str:
        choice = random.choice(data_position['directions'])
        shot = random.randint(0,1)
        if 'br' in data_position['perception']:
            return 'x'
        if ('f' in data_position['perception']) and \
            (self.arrows > 0) and \
            (shot == 0):
            self.arrows -= 1
            choice = choice.lower()
        
        return choice