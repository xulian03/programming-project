from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
from database.repository import RepositoryProvider


# -------------------------------
# Base Abstracta para Serialización
# -------------------------------
class Serializable(ABC):
    """
    Clase abstracta base para las entidades del sistema que deben almacenarse en JSON.
    
    Ofrece métodos de serialización y deserialización para convertir objetos en diccionarios 
    y reconstruirlos después, lo que permite manejar de forma sencilla el guardado y la carga 
    de datos.
    """

    @abstractmethod
    def get_id(self):
        """
        Método abstracto que debe ser implementado por todas las clases hijas.
        Retorna el identificador único de la entidad.
        """
        pass

    def serialize(self):
        """
        Convierte el objeto en un diccionario listo para guardar.

        Se basa en el atributo _serializable_attr, que cada clase define para indicar qué campos deben incluirse.

        Returns:
        dict: Diccionario con los atributos seleccionados del objeto.
        """
        return {attr: getattr(self, attr) for attr in self._serializable_attr}
    
    @classmethod
    def deserialize(cls, data: dict):
        """
        Crea una instancia de la clase a partir de un diccionario.
        
        Remueve los guiones bajos de las claves para hacerlas compatibles
        con los parámetros del constructor.
        
        Args:
            data (dict): Diccionario con los datos del objeto
            
        Returns:
            Instancia de la clase con los datos cargados
        """
        clean_data = {k.lstrip("_"): v for k, v in data.items()}
        obj = cls(**clean_data)
        if not hasattr(obj, "_serializable_attr"):
            obj._serializable_attr = list(data.keys())
        return obj


# -------------------------------
# Enum de posiciones
# -------------------------------
class Position(Enum):
    GK = "GK"
    LD = "LD"
    LI = "LI"
    DFC = "DFC"
    MCD = "MCD"
    MC = "MC"
    LW = "LW"
    MCO = "MCO"
    DC = "DC"
    RW = "RW"


# -------------------------------
# Clase base para Usuarios
# -------------------------------
class User(Serializable):
    def __init__(self, id, name, age, password=None):
        self._id = id
        self._name = name
        self._age = age
        self._password = password
        self._serializable_attr = ["_id", "_name", "_age", "_password"]

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name
    
    def get_age(self):
        return self._age
    
    def set_name(self, name):
        self._name = name
    
    def set_age(self, age):
        self._age = age
    
    def verify_password(self, password):
        return self._password == password


# -------------------------------
# ClubMember (incluye roles como Coach, Staff, Manager, Physio, etc.)
# -------------------------------
class ClubMember(User):
    def __init__(self, id, name, age, password=None, team=None, role=None):
        super().__init__(id, name, age, password)
        self._team = team
        self._role = role
        self._serializable_attr += ["_team", "_role"]

    def get_team(self):
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
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
    def __init__(self, id, name, age, password=None, license=None):
        super().__init__(id, name, age, password)
        self._license = license
        self._serializable_attr += ["_license"]

    def get_license(self):
        return self._license
    
    def set_license(self, license):
        self._license = license


# -------------------------------
# Team
# -------------------------------
class Team(Serializable):
    def __init__(self, id, name, coach=None, players=None, staff=None):
        self._id = id
        self._name = name
        self.coach = coach
        self.players = players or []
        self.staff = staff or []
        self._serializable_attr = ["_id", "_name", "coach", "players", "staff"]

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_coach(self):
        return self.coach

    def set_coach(self, coach_id):
        self.coach = coach_id

    def get_players(self) -> list:
        if self.players and isinstance(self.players[0], str):
            players_repo = RepositoryProvider.get("Player")
            self.players = [players_repo.find(player) for player in self.players]
        return self.players

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player_id):
        if player_id in self.players:
            self.players.remove(player_id)

    def get_staff(self):
        if self.staff and isinstance(self.staff[0], str):
            players_repo = RepositoryProvider.get("Player")
            self.players = [players_repo.find(player) for player in self.players]
        return self.players

    def add_staff(self, staff):
        if staff not in self.staff:
            self.staff.append(staff)

    def remove_staff(self, staff):
        if staff in self.staff:
            self.staff.remove(staff)

    def serialize(self):
        data = super().serialize()
        data["coach"] = self.coach.get_id() if isinstance(self.coach, ClubMember) else self.coach
        data["staff"] = [s.get_id() if isinstance(s, ClubMember) else s for s in self.staff]
        data["players"] = [p.get_id() if isinstance(p, Player) else p for p in self.players]
        return data

    
# -------------------------------
# Player
# -------------------------------
class Player(User):
    def __init__(self, 
                 id, 
                 name, 
                 age, 
                 password=None,
                 team=None, 
                 position=None, 
                 goals=0, 
                 assists=0, 
                 shots=0,   
                 shots_on_target=0, 
                 clearances=0):
        super().__init__(id, name, age, password)
        self._team = team
        self._position = position if isinstance(position, Position) else (Position(position) if position else None)
        self._goals = goals
        self._assists = assists
        self._shots = shots
        self._shots_on_target = shots_on_target
        self._clearances = clearances
        self._serializable_attr += ["_team", "_position", "_goals", "_assists", "_shots", 
                                   "_shots_on_target", "_clearances"]
        
    def get_team(self):
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def set_team(self, team):
        self._team = team
    
    def get_position(self):
        return Position[self._position] if isinstance(self._position, str) else self._position

    def set_position(self, position):
        if not isinstance(position, Position) and not position in Position.__members__:
            raise ValueError("Posición inválida")
        self._position = position if isinstance(position, Position) else Position(position)

    def get_goals(self):
        return self._goals

    def set_goals(self, goals):
        self._goals = goals

    def get_assists(self):
        return self._assists

    def set_assists(self, assists):
        self._assists = assists

    def get_shots(self):
        return self._shots

    def set_shots(self, shots):
        self._shots = shots

    def get_shots_on_target(self):
        return self._shots_on_target

    def set_shots_on_target(self, shots_on_target):
        self._shots_on_target = shots_on_target

    def get_clearances(self):
        return self._clearances

    def set_clearances(self, clearances):
        self._clearances = clearances

    def serialize(self):
        data = super().serialize()
        data["_position"] = self._position.value if self._position else None
        data["_team"] = self._team.get_id() if isinstance(self._team, Team) else self._team
        return data

    @classmethod
    def deserialize(cls, data: dict):
        if "_position" in data and data["_position"]:
            data["_position"] = Position(data["_position"])
        return super().deserialize(data)

# -------------------------------
# Match
# -------------------------------
class Match(Serializable):
    def __init__(self, id, date, home_team, away_team, home_score=0, away_score=0, 
                 referee=None, status="scheduled", player_stats=None, created_by=None, 
                 validated_by=None, notes=""):
        self._id = id
        self._date = date if isinstance(date, datetime) else datetime.fromisoformat(date)
        self._home_team = home_team
        self._away_team = away_team
        self._home_score = home_score
        self._away_score = away_score
        self._referee = referee
        self._status = status
        self._player_stats = player_stats or {}
        self._created_by = created_by
        self._validated_by = validated_by
        self._notes = notes
        self._serializable_attr = ["_id", "_date", "_home_team", "_away_team", "_home_score", 
                                  "_away_score", "_referee", "_status", "_player_stats", 
                                  "_created_by", "_validated_by", "_notes"]

    def get_id(self):
        return self._id

    def get_date(self):
        return self._date
    
    def get_home_team(self):
        return self._home_team

    def get_away_team(self):
        return self._away_team

    def get_home_score(self):
        return self._home_score

    def get_away_score(self):
        return self._away_score
    
    def get_referee(self):
        return self._referee

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_player_stats(self):
        return self._player_stats

    def set_player_stats(self, player_stats):
        self._player_stats = player_stats

    def get_notes(self):
        return self._notes

    def set_notes(self, notes):
        self._notes = notes

    def serialize(self):
        data = super().serialize()
        data["_date"] = self._date.isoformat() if isinstance(self._date, datetime) else self._date
        return data

    @classmethod
    def deserialize(cls, data: dict):
        if "_date" in data and isinstance(data["_date"], str):
            data["_date"] = datetime.fromisoformat(data["_date"])
        return super().deserialize(data)