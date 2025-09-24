from enum import Enum

class Position(Enum):
    GK: 1
    LD: 2
    LI: 3
    DFC: 4
    MCD: 5
    MC: 6
    LW: 7
    MCO: 8
    DC: 9
    RW: 10

class Team():
    def __init__(self):
        self.players = []

    
class User():
    def __init__(self, id, name, age):
        self._id = id
        self._name = name
        self._age = age

    def get_name(self):
        return self.name
    
    def get_age(self):
        return self.age
    
    def set_age(self, age):
        self.age = age

class Player(User):
    def __init__(self, id, name, age, team: Team, squad_num, position: Position):
        super().__init__(id, name, age)
        self._team = team
        self._squad_num = squad_num
        self._position = position
        self._goals = 0
        self._assists = 0
        self._shots = 0
        self._shotsOnTarget = 0
        self._clearances = 0

class Coach(User):
    def __init__(self, id, name, age):
        super().__init__(id, name, age)