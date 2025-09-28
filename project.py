from enum import Enum
from abc import ABC, abstractmethod
from database.repository import RepositoryProvider



class Serializable(ABC):

    @abstractmethod
    def get_id(self):
        pass

    def serialize(self):
        return {attr: getattr(self, attr) for attr in self._serializable_attr}
    
    @classmethod
    def deserialize(cls, data: dict):
        clean_data = {k.lstrip("_"): v for k, v in data.items()}
        obj = cls(**clean_data)
        if not hasattr(obj, "_serializable_attr"):
            obj._serializable_attr = list(data.keys())
        return obj



class Position(Enum):
    GK = 1
    LD = 2
    LI = 3
    DFC = 4
    MCD = 5
    MC = 6
    LW = 7
    MCO = 8
    DC = 9
    RW = 10


class User(Serializable):
    def __init__(self, id, name, age):
        self._id = id
        self._name = name
        self._age = age
        self._serializable_attr = ["_id", "_name", "_age"]

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name
    
    def get_age(self):
        return self._age
    
    def set_age(self, age):
        self._age = age


class Coach(User):
    def __init__(self, id, name, age):
        super().__init__(id, name, age)


class Team(Serializable):
    def __init__(self, id, coach: Coach = None, players=None):
        self._id = id
        self.coach = coach
        self.players: list[Player] = players or []
        self.staff: list = []  
        self._serializable_attr = ["_id", "coach", "players", "staff"]

    def get_id(self):
        return self._id

    def get_players(self) -> list:
        if self.players and isinstance(self.players[0], str):
            players_repo = RepositoryProvider.get("Player")
            self.players = [players_repo.find(player) for player in self.players]
        return self.players

    def serialize(self):
        data = super().serialize()
        data["coach"] = self.coach.get_id() if self.coach else None
        data["players"] = [player.get_id() for player in self.players]
        return data
    
    @classmethod
    def deserialize(cls, data):
        obj = super().deserialize(data)
        return obj


class Player(User):
    def __init__(
        self, 
        id, 
        name, 
        age, 
        team: Team, 
        squad_num, 
        position: Position, 
        goals=0, 
        assists=0, 
        shots=0, 
        shotsOnTarget=0, 
        clearances=0
    ):
        super().__init__(id, name, age)
        self._team = team
        self._squad_num = squad_num
        self._position = position
        self._goals = goals
        self._assists = assists
        self._shots = shots
        self._shotsOnTarget = shotsOnTarget
        self._clearances = clearances
        self._serializable_attr += [
            "_team", "_squad_num", "_position",
            "_goals", "_assists", "_shots",
            "_shotsOnTarget", "_clearances"
        ]
    
    def get_team(self):
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def get_position(self):
        return Position[self._position]

    def serialize(self):
        data = super().serialize()
        data["_team"] = self._team.get_id()
        data["_position"] = self._position.name
        return data



class Match:
    def __init__(self, date, rival, goals, assists, minutes):
        self.date = date 
        self.rival = rival 
        self.goals = goals 
        self.assists = assists 
        self.minutes = minutes


class ClubMember(User):
    def __init__(self, id, name, age, team_coach, role):
        super().__init__(id, name, age)
        self._team_coach = team_coach
        self._role = role
        self._serializable_attr += ["_team_coach", "_role"]

    def get_team_coach(self):
        return self._team_coach
    
    def set_team_coach(self, team_coach):
        self._team_coach = team_coach 
    
    def get_role(self):
        return self._role
    
    def set_role(self, role):
        self._role = role


class Referee(User):
    def __init__(self, id, name, age, licencia):
        super().__init__(id, name, age)
        self.__licencia = licencia
        self._serializable_attr += ["__licencia"]
    
    def get_licencia(self):
        return self.__licencia  
    
    def set_licencia(self, licencia):
        self.__licencia = licencia



