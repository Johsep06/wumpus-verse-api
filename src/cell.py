class Cell:
    UNKNOW = 'unknow'
    KNOW = 'know'
    WUMPUS = 'wumpus'
    HOLE = 'hole'
    GOLD = 'gold'
    EXIT = 'exit'

    WUMPUS_SUSPECT = 'wumpus'
    HOLE_SUSPECT = 'hole'
    HOLE_AND_WUMPUS_SUSPECT = 'hole_wumpus'

    def __init__(self, object_: str = None):
        self._is_safe = False
        self.objetcs = set()
        self.suspects = set()

        if object_ is None:
            self.objetcs.add(self.UNKNOW)
        else:
            self.add_object(object_)

    @property
    def is_safe(self) -> bool:
        return self._is_safe

    @is_safe.setter
    def is_safe(self, value: bool):
        if value:
            self.suspects.clear()

        self._is_safe = value
    
    def __repr__(self):
        return f'<Cell safe:{self._is_safe}, obj:{self.objetcs}, susp:{self.suspects}>'

    def add_object(self, object_: str):
        #! Lembrar de retornar um erro caso o objeto seja inválido
        if object_ != self.UNKNOW:
            self.suspects.clear()
        
        if len(self.objetcs) == 0:
            self.objetcs.add(object_)
            return True

        elif self.objetcs == {self.UNKNOW}:
            self.objetcs.clear()
            self.objetcs.add(object_)
            return True

        elif self.objetcs == {self.KNOW}:
            self.objetcs.clear()
            self.objetcs.add(object_)
            return True

        elif self.objetcs == {self.EXIT}:
            return False

        elif object_ == self.UNKNOW:
            return False

        elif object_ == self.KNOW:
            return False
        
        elif object_ == self.EXIT:
            self.is_safe = True 
            return True

        else:
            self.objetcs.add(object_)
            return True

    def add_suspect(self, suspect: str):
        is_hole = suspect == self.HOLE_SUSPECT
        is_wumpus = suspect == self.WUMPUS_SUSPECT
        is_hole_and_wumpus = suspect == self.HOLE_AND_WUMPUS_SUSPECT
        
        if not (is_hole or is_wumpus or is_hole_and_wumpus):
            raise ValueError('o valor informado não é valido')
        
        if self._is_safe:
            return True

        elif len(self.suspects) == 0:
            self.suspects.add(suspect)
            self._is_safe = False
            return False

        elif suspect not in self.suspects:
            self.suspects.clear()
            self._is_safe = True
            return True

        else:
            self.suspects.add(suspect)
            return False
