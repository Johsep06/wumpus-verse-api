from abc import ABC, abstractmethod
import random


class Agent(ABC):
    def __init__(self, tag: str, position:tuple[int, int]):
        self.tag = tag
        self.type = -1
        self.game_over = False
        self.__status = ''
        self.pts = 0
        self.position = position
        self.start_position = position
        self.gold = 0
        
    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str):
        self.__status = status

        for value in ['W', 'P']: 
            if value in status:
                self.game_over = True
        
        if (self.position == self.start_position) and (self.gold > 0):
            self.game_over = True
            self.__status = 'V'

    def __str__(self):
        return f'Agent(tag={self.tag}, type:{self.type}, pts={self.pts}, game_over={self.game_over})'

    def update_pts(self):
        if self.__status == 'W':
            self.pts -= 1000
        elif self.__status == 'P':
            self.pts -= 1000
        elif self.__status == 'V':
            self.pts += 1000
        elif self.__status == 'T':
            self.pts += 1000
        elif self.__status == 't':
            self.pts -= 10
            
    def set_position(self, x: int, y: int):
        self.position = (x, y)
    
    def get_position(self) -> tuple[int, int]:
        return self.position

    @abstractmethod
    def execute(self, data_position: dict): ...