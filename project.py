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
        # Remueve el underscore inicial de las claves para que coincidan
        # con los nombres de parámetros del constructor
        clean_data = {k.lstrip("_"): v for k, v in data.items()}
        obj = cls(**clean_data)
        # Preserva la lista de atributos serializables si no existe
        if not hasattr(obj, "_serializable_attr"):
            obj._serializable_attr = list(data.keys())
        return obj


# -------------------------------
# Enum de posiciones
# -------------------------------
class Position(Enum):
    """
    Enumeración de posiciones válidas en el campo de fútbol.
    
    Garantiza consistencia en los datos y previene errores de tipeo al
    limitar las posiciones a valores predefinidos.
    """
    GK = "GK"   # Portero (Goalkeeper)
    LD = "LD"   # Lateral Derecho
    LI = "LI"   # Lateral Izquierdo
    DFC = "DFC" # Defensa Central
    MCD = "MCD" # Medio Centro Defensivo
    MC = "MC"   # Medio Centro
    LW = "LW"   # Extremo Izquierdo (Left Wing)
    MCO = "MCO" # Medio Centro Ofensivo
    DC = "DC"   # Delantero Centro
    RW = "RW"   # Extremo Derecho (Right Wing)


# -------------------------------
# Clase base para Usuarios
# -------------------------------
class User(Serializable):
    """
    Clase base para todos los tipos de usuario del sistema.
    
    Centraliza atributos y funcionalidad común a jugadores, entrenadores y
    árbitros, evitando duplicación de código y facilitando la autenticación.
    
    Attributes:
    _id (str): Identificador único del usuario
    _name (str): Nombre completo del usuario
    _age (int): Edad del usuario
    _password (str): Contraseña del usuario (debe ser encriptada antes de almacenar)
    """
    def __init__(self, id, name, age, password=None):
        """
        Constructor de la clase User.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad del usuario
        password (str, optional): Contraseña. Por defecto None
        """
        self._id = id
        self._name = name
        self._age = age
        self._password = password
        # Define qué atributos se incluirán en la serialización
        self._serializable_attr = ["_id", "_name", "_age", "_password"]

    def get_id(self):
        """Retorna el ID único del usuario."""
        return self._id

    def get_name(self):
        """Retorna el nombre del usuario."""
        return self._name
    
    def get_age(self):
        """Retorna la edad del usuario."""
        return self._age
    
    def set_name(self, name):
        """
        Actualiza el nombre del usuario.
        
        Args:
        name (str): Nuevo nombre
        """
        self._name = name
    
    def set_age(self, age):
        """
        Actualiza la edad del usuario.
        
        Args:
        age (int): Nueva edad
        """
        self._age = age
    
    def verify_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        
        Args:
        password (str): Contraseña a verificar
            
        Returns:
        bool: True si las contraseñas coinciden, False en caso contrario
        """
        return self._password == password


# -------------------------------
# ClubMember (incluye roles como Coach, Staff, Manager, Physio, etc.)
# -------------------------------
class ClubMember(User):
    """
    Representa a miembros del cuerpo técnico de un equipo.
    
    Incluye entrenadores, preparadores físicos, staff administrativo, etc.
    El atributo _role permite diferenciar entre los distintos tipos de personal.
    
    Attributes:
    _team (str): ID del equipo al que pertenece (puede ser None al inicio)
    _role (str): Rol dentro del club ("coach", "staff", "manager", "physio")
    """
    def __init__(self, id, name, age, password=None, team=None, role=None):
        """
        Constructor de ClubMember.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad
        password (str, optional): Contraseña
        team (str, optional): ID del equipo
        role (str, optional): Rol dentro del club
        """
        super().__init__(id, name, age, password)
        self._team = team
        self._role = role
        # Agrega atributos específicos a la lista de serialización
        self._serializable_attr += ["_team", "_role"]

    def get_team(self):
        """
        Retorna el objeto Team asociado a este miembro.
        
        Si _team es solo un ID (string), lo convierte en objeto Team
        consultando el repositorio. Esto implementa lazy loading para
        optimizar el uso de memoria.
        
        Returns:
        Team: Objeto del equipo al que pertenece
        """
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def set_team(self, team):
        """
        Asigna un equipo a este miembro del club.
        
        Args:
        team (str|Team): ID del equipo u objeto Team
        """
        self._team = team 
    
    def get_role(self):
        """Retorna el rol del miembro dentro del club."""
        return self._role
    
    def set_role(self, role):
        """
        Actualiza el rol del miembro.
        
        Args:
        role (str): Nuevo rol
        """
        self._role = role
    
    def serialize(self):
        """
        Serializa el miembro de club a diccionario.
        
        Convierte el objeto Team a ID para
        permitir almacenamiento en JSON.
        
        Returns:
        dict: Diccionario serializable del jugador
        """
        data = super().serialize()
        # Convierte objeto Team a ID
        data["_team"] = self._team.get_id() if isinstance(self._team, Team) else self._team
        return data


# -------------------------------
# Referee
# -------------------------------
class Referee(User):
    """
    Representa a un árbitro del sistema.
    
    Los árbitros tienen permisos especiales para validar estadísticas de
    partidos y acceder a información de todos los equipos y jugadores.
    
    Attributes:
    _license (str): Número de licencia único que identifica al árbitro
    """
    def __init__(self, id, name, age, password=None, license=None):
        """
        Constructor de Referee.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad
        password (str, optional): Contraseña
        license (str, optional): Número de licencia único
        """
        super().__init__(id, name, age, password)
        self._license = license
        self._serializable_attr += ["_license"]

    def get_license(self):
        """Retorna el número de licencia del árbitro."""
        return self._license
    
    def set_license(self, license):
        """
        Actualiza el número de licencia.
        
        Args:
        license (str): Nueva licencia
        """
        self._license = license


# -------------------------------
# Team
# -------------------------------
class Team(Serializable):
    """
    Representa un equipo de fútbol en el sistema.
    
    Agrupa jugadores bajo la supervisión de un entrenador y permite
    gestionar la organización del personal técnico. Es fundamental para
    el control de permisos (usuarios solo pueden ver información de su equipo).
    
    Attributes:
    _id (str): Identificador único del equipo
    _name (str): Nombre del equipo
    coach (str): ID del entrenador principal
    players (list): Lista de IDs de jugadores
    staff (list): Lista de IDs del personal técnico
    """
    def __init__(self, id, name, coach=None, players=None, staff=None):
        """
        Constructor de Team.
        
        Args:
        id (str): Identificador único
        name (str): Nombre del equipo
        coach (str, optional): ID del entrenador
        players (list, optional): Lista de IDs de jugadores
        staff (list, optional): Lista de IDs del staff
        """
        self._id = id
        self._name = name
        self.coach = coach
        # Inicializa listas vacías si no se proporcionan
        self.players = players or []
        self.staff = staff or []
        self._serializable_attr = ["_id", "_name", "coach", "players", "staff"]

    def get_id(self):
        """Retorna el ID del equipo."""
        return self._id

    def get_name(self):
        """Retorna el nombre del equipo."""
        return self._name

    def set_name(self, name):
        """
        Actualiza el nombre del equipo.
        
        Args:
        name (str): Nuevo nombre
        """
        self._name = name

    def get_coach(self):
        """Retorna el ID o objeto del entrenador del equipo."""
        return self.coach

    def set_coach(self, coach_id):
        """
        Asigna un entrenador al equipo.
        
        Args:
        coach_id (str): ID del entrenador
        """
        self.coach = coach_id

    def get_players(self) -> list:
        """
        Retorna la lista de jugadores del equipo.
        
        Si los jugadores están almacenados como IDs, los convierte en
        objetos Player consultando el repositorio (lazy loading).
        
        Returns:
        list: Lista de objetos Player
        """
        if self.players and isinstance(self.players[0], str):
            players_repo = RepositoryProvider.get("Player")
            self.players = [players_repo.find(player) for player in self.players]
        return self.players

    def add_player(self, player):
        """
        Agrega un jugador al equipo.
        
        Args:
        player (str|Player): ID del jugador u objeto Player
            
        Note:
        Previene duplicados verificando si el jugador ya existe
        """
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player_id):
        """
        Elimina un jugador del equipo.
        
        Args:
        player_id (str): ID del jugador a eliminar
        """
        if player_id in self.players:
            self.players.remove(player_id)

    def get_staff(self):
        """
        Retorna la lista del personal técnico del equipo.
        
        Returns:
        list: Lista de objetos ClubMember
        """
        if self.staff and isinstance(self.staff[0], str):
            players_repo = RepositoryProvider.get("ClubMember")
            self.players = [players_repo.find(player) for player in self.players]
        return self.staff

    def add_staff(self, staff):
        """
        Agrega un miembro al staff técnico.
        
        Args:
        staff (str|ClubMember): ID o objeto del miembro del staff
        """
        if staff not in self.staff:
            self.staff.append(staff)

    def remove_staff(self, staff):
        """
        Elimina un miembro del staff técnico.
        
        Args:
        staff (str): ID del miembro a eliminar
        """
        if staff in self.staff:
            self.staff.remove(staff)

    def serialize(self):
        """
        Serializa el equipo a diccionario.
        
        Convierte objetos anidados (coach, players, staff) a sus IDs
        para evitar serialización recursiva infinita.
        
        Returns:
        dict: Diccionario serializable del equipo
        """
        data = super().serialize()
        # Convierte objetos a IDs si es necesario
        data["coach"] = self.coach.get_id() if isinstance(self.coach, ClubMember) else self.coach
        data["staff"] = [s.get_id() if isinstance(s, ClubMember) else s for s in self.staff]
        data["players"] = [p.get_id() if isinstance(p, Player) else p for p in self.players]
        return data

    
# -------------------------------
# Player
# -------------------------------
class Player(User):
    """
    Representa a un jugador de fútbol en el sistema.
    
    Extiende User agregando estadísticas deportivas y atributos específicos
    del rendimiento en campo. Estas métricas son utilizadas por entrenadores
    para evaluar y comparar jugadores.
    
    Attributes:
    _team (str): ID del equipo al que pertenece
    _position (Position): Posición en el campo (usando enum)
    _goals (int): Total de goles anotados
    _assists (int): Total de asistencias
    _shots (int): Total de disparos realizados
    _shots_on_target (int): Disparos que fueron al arco
    _clearances (int): Total de despejes (relevante para defensas)
    """
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
        """
        Constructor de Player.
        
        Args:
        id (str): Identificador único
        name (str): Nombre completo
        age (int): Edad
        password (str, optional): Contraseña
        team (str, optional): ID del equipo
        position (Position|str, optional): Posición en el campo
        goals (int, optional): Goles anotados. Por defecto 0
        assists (int, optional): Asistencias. Por defecto 0
        shots (int, optional): Disparos totales. Por defecto 0
        shots_on_target (int, optional): Disparos al arco. Por defecto 0
        clearances (int, optional): Despejes. Por defecto 0
        """
        super().__init__(id, name, age, password)
        self._team = team
        # Maneja conversión automática de string a enum Position
        self._position = position if isinstance(position, Position) else (Position(position) if position else None)
        self._goals = goals
        self._assists = assists
        self._shots = shots
        self._shots_on_target = shots_on_target
        self._clearances = clearances
        # Registra atributos específicos para serialización
        self._serializable_attr += ["_team", "_position", "_goals", "_assists", "_shots", 
                                   "_shots_on_target", "_clearances"]
        
    def get_team(self):
        """
        Retorna el objeto Team del jugador.
        
        Implementa lazy loading: si _team es un ID, lo convierte en objeto.
        
        Returns:
        Team: Equipo al que pertenece el jugador
        """
        if isinstance(self._team, str):
            teams_repo = RepositoryProvider.get("Team")
            self._team = teams_repo.find(self._team)
        return self._team
    
    def set_team(self, team):
        """
        Asigna un equipo al jugador.
        
        Args:
        team (str|Team): ID del equipo u objeto Team
        """
        self._team = team
    
    def get_position(self):
        """
        Retorna la posición del jugador como enum.
        
        Convierte string a enum si es necesario para mantener consistencia.
        
        Returns:
        Position: Posición del jugador
        """
        return Position[self._position] if isinstance(self._position, str) else self._position

    def set_position(self, position):
        """
        Actualiza la posición del jugador.
        
        Args:
        position (Position|str): Nueva posición
        """
        if not isinstance(position, Position) and not position in Position.__members__:
            raise ValueError("Posición inválida")
        self._position = position if isinstance(position, Position) else Position(position)
    # Getters y setters para estadísticas
    def get_goals(self):
        """Retorna el total de goles anotados."""
        return self._goals

    def set_goals(self, goals):
        """
        Actualiza el total de goles.
        
        Args:
        goals (int): Nuevo total de goles
        """
        self._goals = goals

    def get_assists(self):
        """Retorna el total de asistencias."""
        return self._assists

    def set_assists(self, assists):
        """
        Actualiza el total de asistencias.
        
        Args:
        assists (int): Nuevo total de asistencias
        """
        self._assists = assists

    def get_shots(self):
        """Retorna el total de disparos realizados."""
        return self._shots

    def set_shots(self, shots):
        """
        Actualiza el total de disparos.
        
        Args:
        shots (int): Nuevo total de disparos
        """
        self._shots = shots

    def get_shots_on_target(self):
        """Retorna el total de disparos al arco."""
        return self._shots_on_target

    def set_shots_on_target(self, shots_on_target):
        """
        Actualiza el total de disparos al arco.
        
        Args:
        shots_on_target (int): Nuevo total
        """
        self._shots_on_target = shots_on_target

    def get_clearances(self):
        """Retorna el total de despejes (métrica defensiva)."""
        return self._clearances

    def set_clearances(self, clearances):
        """
        Actualiza el total de despejes.
        
        Args:
        clearances (int): Nuevo total de despejes
        """
        self._clearances = clearances

    def serialize(self):
        """
        Serializa el jugador a diccionario.
        
        Convierte el enum Position a string y el objeto Team a ID para
        permitir almacenamiento en JSON.
        
        Returns:
        dict: Diccionario serializable del jugador
        """
        data = super().serialize()
        # Convierte enum a valor string
        data["_position"] = self._position.value if self._position else None
        # Convierte objeto Team a ID
        data["_team"] = self._team.get_id() if isinstance(self._team, Team) else self._team
        return data

    @classmethod
    def deserialize(cls, data: dict):
        """
        Crea un objeto Player desde un diccionario.
        
        Convierte el string de posición de vuelta a enum Position.
        
        Args:
        data (dict): Datos serializados del jugador
            
        Returns:
        Player: Instancia de jugador con datos cargados
        """
        # Convierte string a enum antes de crear el objeto
        if "_position" in data and data["_position"]:
            data["_position"] = Position(data["_position"])
        return super().deserialize(data)

# -------------------------------
# Match
# -------------------------------
class Match(Serializable):
    """
    Representa un partido de fútbol.
    
    Esta clase está preparada para funcionalidades futuras donde se registren
    y validen partidos, incluyendo estadísticas detalladas de cada jugador.
    
    Attributes:
    _id (str): Identificador único del partido
    _date (datetime): Fecha y hora del partido
    _home_team (str): ID del equipo local
    _away_team (str): ID del equipo visitante
    _home_score (int): Goles del equipo local
    _away_score (int): Goles del equipo visitante
    _referee (str): ID del árbitro que dirige el partido
    _status (str): Estado del partido ("scheduled", "finished", "validated")
    _player_stats (dict): Estadísticas individuales de jugadores
    _created_by (str): ID del usuario que creó el registro
    _validated_by (str): ID del árbitro que validó el partido
    _notes (str): Notas adicionales sobre el partido
    """
    def __init__(self, id, date, home_team, away_team, home_score=0, away_score=0, 
                 referee=None, status="scheduled", player_stats=None, created_by=None, 
                 validated_by=None, notes=""):
        """
        Constructor de Match.
        
        Args:
        id (str): Identificador único
        date (datetime|str): Fecha del partido (ISO format si es string)
        home_team (str): ID del equipo local
        away_team (str): ID del equipo visitante
        home_score (int, optional): Goles local. Por defecto 0
        away_score (int, optional): Goles visitante. Por defecto 0
        referee (str, optional): ID del árbitro
        status (str, optional): Estado inicial. Por defecto "scheduled"
        player_stats (dict, optional): Estadísticas por jugador
        created_by (str, optional): ID del creador
        validated_by (str, optional): ID del validador
        notes (str, optional): Notas adicionales
        """
        self._id = id
        # Convierte string ISO a datetime si es necesario
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
    # Getters básicos
    def get_id(self):
        """Retorna el ID del partido."""
        return self._id

    def get_date(self):
        """Retorna la fecha del partido."""
        return self._date
    
    def get_home_team(self):
        """Retorna el ID del equipo local."""
        return self._home_team

    def get_away_team(self):
        """Retorna el ID del equipo visitante."""
        return self._away_team

    def get_home_score(self):
        """Retorna los goles del equipo local."""
        return self._home_score

    def get_away_score(self):
        """Retorna los goles del equipo visitante."""
        return self._away_score
    
    def get_referee(self):
        """Retorna el ID del árbitro."""
        return self._referee

    def get_status(self):
        """Retorna el estado actual del partido."""
        return self._status

    def set_status(self, status):
        """
        Actualiza el estado del partido.
        
        Args:
        status (str): Nuevo estado ("scheduled", "finished", "validated")
        """
        self._status = status

    def get_player_stats(self):
        """Retorna el diccionario de estadísticas por jugador."""
        return self._player_stats

    def set_player_stats(self, player_stats):
        """
        Actualiza las estadísticas de jugadores del partido.
        
        Args:
        player_stats (dict): Diccionario {player_id: {stat: value}}
        """
        self._player_stats = player_stats

    def get_notes(self):
        """Retorna las notas del partido."""
        return self._notes

    def set_notes(self, notes):
        """
        Actualiza las notas del partido.
        
        Args:
        notes (str): Nuevas notas
        """
        self._notes = notes

    def serialize(self):
        """
        Serializa el partido a diccionario.
        
        Convierte datetime a string ISO format para permitir almacenamiento JSON.
        
        Returns:
        dict: Diccionario serializable del partido
        """
        data = super().serialize()
        # Convierte datetime a ISO format string
        data["_date"] = self._date.isoformat() if isinstance(self._date, datetime) else self._date
        return data

    @classmethod
    def deserialize(cls, data: dict):
        """
        Crea un objeto Match desde un diccionario.
        
        Convierte el string ISO de fecha de vuelta a datetime.
        
        Args:
        data (dict): Datos serializados del partido
            
        Returns:
        Match: Instancia de partido con datos cargados
        """
        # Convierte ISO string a datetime
        if "_date" in data and isinstance(data["_date"], str):
            data["_date"] = datetime.fromisoformat(data["_date"])
        return super().deserialize(data)