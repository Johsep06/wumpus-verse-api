from abc import ABC, abstractmethod
import random


class Agent(ABC):
    def __init__(self, tag: str, position:tuple[int, int]):
        self.tag = tag
        self.type = -1
        self.game_over = False
        self._status = ''
        self.pts = 0
        self.position = position
        self.start_position = position
        self.gold = 0
        self.arrows= 0
        self.action_queue:list[str] = []
        
    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str):
        self._status = status

        for value in ['W', 'P']: 
            if value in status:
                self.game_over = True
        
        if (self.position == self.start_position) and (self.gold > 0):
            self.game_over = True
            self._status = 'V'

    def __str__(self):
        return f'Agent(tag={self.tag}, type:{self.type}, pts={self.pts}, game_over={self.game_over})'

    def update_pts(self):
        self.pts -= 1
        if 'W' in self._status:
            self.pts -= 1000
        elif 'P' in self._status:
            self.pts -= 1000
        elif 'x' in self._status:
            self.gold += 1
            self.pts += 1000
        elif 'T' in self._status:
            self.pts += 1000
        elif 't' in self._status:
            self.pts -= 10
            
    def set_position(self, x: int, y: int):
        self.position = (x, y)
    
    def get_position(self) -> tuple[int, int]:
        return self.position

    @abstractmethod
    def execute(self, data_position: dict) -> str: ...