from enum import Enum
from abc import ABC, abstractmethod
from database.repository import RepositoryProvider


# -------------------------------
# Base Abstracta para Serialización
# -------------------------------
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


# -------------------------------
# Enum de posiciones
# -------------------------------
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


# -------------------------------
# Clase base para Usuarios
# -------------------------------
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


# -------------------------------
# ClubMember (incluye roles como Coach, Médico, Preparador, etc.)
# -------------------------------
class ClubMember(User):
    def __init__(self, id, name, age, team=None, role=None):
        super().__init__(id, name, age)
        self._team = team
        self._role = role
        self._serializable_attr += ["_team", "_role"]

    def get_team(self):
        return self._team
    
    def set_team(self, team):
        self._team = team 
    
    def get_role(self):
        return self._role
    
    def set_role(self, role):
        self._role = role


# -------------------------------
# Referee
# -------------------------------
class Referee(User):
    def __init__(self, id, name, age, licencia):
        super().__init__(id, name, age)
        self.__licencia = licencia 
        self._serializable_attr += ["_Referee__licencia"]

    def get_licencia(self):
        return self.__licencia  
    
    def set_licencia(self, licencia):
        self.__licencia = licencia


# -------------------------------
# Team
# -------------------------------
class Team(Serializable):
    def __init__(self, id, coach: ClubMember = None, players=None):
        self._id = id
        self._coach = coach
        self._players: list[Player] = players or []
        self._serializable_attr = ["_id", "_coach", "_players"]

    def get_id(self):
        return self._id

    def get_coach(self):
        return self._coach

    def get_players(self) -> list:
        if self._players and isinstance(self._players[0], str):
            players_repo = RepositoryProvider.get("Player")
            self._players = [players_repo.find(player) for player in self._players]
        return self._players

    def serialize(self):
        data = super().serialize()
        data["_coach"] = self._coach.get_id() if self._coach else None
        data["_players"] = [player.get_id() for player in self._players]
        return data
    
    @classmethod
    def deserialize(cls, data):
        obj = super().deserialize(data)
        return obj


# -------------------------------
# Player
# -------------------------------
class Player(User):
    def __init__(self, 
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
                 clearances=0):
        super().__init__(id, name, age)
        self._team = team
        self._squad_num = squad_num
        self._position = position
        self._goals = goals
        self._assists = assists
        self._shots = shots
        self._shotsOnTarget = shotsOnTarget
        self._clearances = clearances
        self._serializable_attr += ["_team", "_squad_num", "_position", 
                                   "_goals", "_assists", "_shots", 
                                   "_shotsOnTarget", "_clearances"]
        
    def get_team(self):
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def get_position(self):
        return Position[self._position] if isinstance(self._position, str) else self._position

    def serialize(self):
        data = super().serialize()
        data["_team"] = self._team.get_id() if self._team else None
        data["_position"] = self._position.name if isinstance(self._position, Position) else self._position
        return data


# -------------------------------
# Match
# -------------------------------
class Match(Serializable):
    def __init__(self, id, date, rival, goals, assists, minutes):
        self._id = id
        self._date = date
        self._rival = rival
        self._goals = goals
        self._assists = assists
        self._minutes = minutes
        self._serializable_attr = ["_id", "_date", "_rival", "_goals", "_assists", "_minutes"]

    def get_id(self):
        return self._id

    def get_date(self):
        return self._date
    
    def get_rival(self):
        return self._rival

    def get_goals(self):
        return self._goals
    
    def get_assists(self):
        return self._assists
    
    def get_minutes(self):
        return self._minutes
