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


# ==============================
# Enumeraciones
# ==============================
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


# ==============================
# Entidades
# ==============================
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
    
    def set_age(self, age):
        self._age = age

    def set_name(self, name):
        self._name = name

    def set_password(self, password):
        self._password = password

    def check_password(self, password):
        return self._password == password


class Team(Serializable):
    def __init__(self, id, coach: "ClubMember" = None, players=None):
        self._id = id
        self.coach = coach
        self.players: list[Player] = players or []
        self.staff: list[ClubMember] = []  
        self._serializable_attr = ["_id", "coach", "players", "staff"]

    def get_id(self):
        return self._id

    def get_coach(self):
        if isinstance(self.coach, str):
            coach_repo = RepositoryProvider.get("ClubMember")
            self.coach = coach_repo.find(self.coach)
        return self.coach

    def set_coach(self, coach: "ClubMember"):
        self.coach = coach

    def get_players(self) -> list:
        if self.players and isinstance(self.players[0], str):
            players_repo = RepositoryProvider.get("Player")
            self.players = [players_repo.find(player) for player in self.players]
        return self.players

    def add_player(self, player: "Player"):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self, player: "Player"):
        if player in self.players:
            self.players.remove(player)

    def get_staff(self) -> list:
        return self.staff

    def add_staff(self, staff_member: "ClubMember"):
        if staff_member not in self.staff:
            self.staff.append(staff_member)

    def remove_staff(self, staff_member: "ClubMember"):
        if staff_member in self.staff:
            self.staff.remove(staff_member)

    def serialize(self):
        data = super().serialize()
        data["coach"] = self.coach.get_id() if isinstance(self.coach, ClubMember) else None
        data["players"] = [player.get_id() for player in self.players if isinstance(player, Player)]
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
        password=None,
        team_id=None, 
        squad_num=None, 
        position: Position = None, 
        goals=0, 
        assists=0
    ):
        super().__init__(id, name, age, password)
        self.team_id = team_id
        self._squad_num = squad_num
        self._position = position
        self.stats = {"goles": goals, "asistencias": assists, "partidos": 0}
        self.history = []
        self._serializable_attr += [
            "team_id", "_squad_num", "_position", "stats", "history"
        ]
    
    def get_position(self):
        return Position[self._position] if isinstance(self._position, str) else self._position

    def set_position(self, position):
        self._position = position

    def add_match(self, rival, resultado):
        self.history.append({"rival": rival, "resultado": resultado})
        self.stats["partidos"] += 1

    def serialize(self):
        data = super().serialize()
        data["team_id"] = self.team_id
        data["_position"] = self._position.name if isinstance(self._position, Position) else self._position
        return data


class Match(Serializable):
    def __init__(self, id, date, rival, goals, assists, minutes):
        self._id = id
        self.date = date 
        self.rival = rival 
        self.goals = goals 
        self.assists = assists 
        self.minutes = minutes
        self._serializable_attr = ["_id", "date", "rival", "goals", "assists", "minutes"]

    def get_id(self):
        return self._id


class ClubMember(User):
    def __init__(self, id, name, age, password=None, team_id=None, role=None):
        super().__init__(id, name, age, password)
        self.team_id = team_id
        self.role = role
        self._serializable_attr += ["team_id", "role"]


class Referee(User):
    def __init__(self, id, name, age, password=None, licencia=None):
        super().__init__(id, name, age, password)
        self.__licencia = licencia
        self.assigned_matches = []
        self._serializable_attr += ["__licencia", "assigned_matches"]
    
    def get_licencia(self):
        return self.__licencia  
    
    def set_licencia(self, licencia):
        self.__licencia = licencia      


class ScoutingError(Exception):
    pass

class ValidationError(ScoutingError):
    pass

class AuthenticationError(ScoutingError):
    pass

class AuthService:
    def __init__(self):
        self.players = {}
        self.club_members = {}
        self.referees = {}
        self.logged_user = None

    def register(self, user_type, user_id, name, age, password, team_id=None):
        if len(password) < 6:
            raise ValidationError("La contraseña debe tener al menos 6 caracteres.")
        if not (10 <= age <= 60):
            raise ValidationError("La edad debe estar entre 10 y 60 años.")

        if user_type == "player":
            if user_id in self.players:
                raise ValidationError("Jugador ya registrado.")
            self.players[user_id] = Player(user_id, name, age, password, team_id)
        elif user_type == "club_member":
            if user_id in self.club_members:
                raise ValidationError("Miembro de club ya registrado.")
            self.club_members[user_id] = ClubMember(user_id, name, age, password, team_id)
        elif user_type == "referee":
            if user_id in self.referees:
                raise ValidationError("Árbitro ya registrado.")
            self.referees[user_id] = Referee(user_id, name, age, password)
        else:
            raise ValidationError("Tipo de usuario inválido.")

        return f"{user_type} registrado con éxito."

    def login(self, user_id, password, user_type):
        if user_type == "player":
            user = self.players.get(user_id)
        elif user_type == "club_member":
            user = self.club_members.get(user_id)
        else:
            user = self.referees.get(user_id)

        if not user:
            raise AuthenticationError("Usuario no encontrado.")
        if not user.check_password(password):
            raise AuthenticationError("Contraseña incorrecta.")

        self.logged_user = user
        return user

    def logout(self):
        self.logged_user = None


# ==============================
# Servicios específicos
# ==============================
class PlayerService:
    def view_stats(self, player: Player):
        return player.stats

    def view_team(self, player: Player):
        return player.team_id if player.team_id else "Sin equipo asignado"

    def view_history(self, player: Player):
        return player.history if player.history else "No hay historial."

    def update_profile(self, player: Player, name, age):
        if not (10 <= age <= 60):
            raise ValidationError("Edad inválida.")
        player.set_name(name)
        player.set_age(age)
        return "Perfil actualizado."


class MemberService:
    def view_team_players(self, member: ClubMember, auth: AuthService):
        jugadores = [p for p in auth.players.values() if p.team_id == member.team_id]
        if not jugadores:
            raise ValidationError("No hay jugadores en este equipo.")
        return jugadores

    def update_player_stats(self, member: ClubMember, auth: AuthService, player_id, goles, asistencias, partidos):
        if player_id not in auth.players:
            raise ValidationError("Jugador no encontrado.")
        player = auth.players[player_id]
        if player.team_id != member.team_id:
            raise ValidationError("No puedes modificar jugadores de otro equipo.")
        player.stats["goles"] += goles
        player.stats["asistencias"] += asistencias
        player.stats["partidos"] += partidos
        return f"Estadísticas de {player.get_name()} actualizadas."

    def create_match_report(self, member: ClubMember, rival, resultado, auth: AuthService):
        jugadores = [p for p in auth.players.values() if p.team_id == member.team_id]
        for p in jugadores:
            p.add_match(rival, resultado)
        return "Reporte de partido creado."

    def view_profile(self, member: ClubMember):
        return {
            "ID": member.get_id(),
            "Nombre": member.get_name(),
            "Edad": member.get_age(),
            "Rol": member.role,
            "Equipo": member.team_id
        }


class RefereeService:
    def assign_match(self, referee: Referee, partido):
        referee.assigned_matches.append(partido)

    def view_matches(self, referee: Referee):
        return referee.assigned_matches if referee.assigned_matches else "No tienes partidos asignados."

    def report_result(self, referee: Referee, partido, resultado):
        for m in referee.assigned_matches:
            if m["id"] == partido:
                m["resultado"] = resultado
                return "Resultado reportado."
        raise ValidationError("Partido no encontrado.")

    def view_profile(self, referee: Referee):
        return {
            "ID": referee.get_id(),
            "Nombre": referee.get_name(),
            "Edad": referee.get_age()
        }

class MenuSystem:
    def __init__(self):
        self.auth_service = AuthService()
        self.player_service = PlayerService()
        self.club_service = MemberService()
        self.referee_service = RefereeService()

    def main_menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Salir")
            opcion = input("Selecciona: ")

            try:
                if opcion == "1":
                    self.register_menu()
                elif opcion == "2":
                    self.login_menu()
                elif opcion == "3":
                    print("Hasta luego 👋")
                    break
                else:
                    print("Opción inválida.")
            except ScoutingError as e:
                print(f"Error: {e}")

    def register_menu(self):
        print("\n=== REGISTRO ===")
        tipo = input("Tipo (player / club_member / referee): ")
        user_id = input("ID: ")
        name = input("Nombre: ")
        age = int(input("Edad: "))
        password = input("Contraseña: ")
        team_id = None
        if tipo in ["player", "club_member"]:
            team_id = input("ID del equipo: ")
        msg = self.auth_service.register(tipo, user_id, name, age, password, team_id)
        print(msg)

    def login_menu(self):
        print("\n=== LOGIN ===")
        tipo = input("Tipo (player / club_member / referee): ")
        user_id = input("ID: ")
        password = input("Contraseña: ")
        user = self.auth_service.login(user_id, password, tipo)
        print(f"Bienvenido {user.get_name()}!")

        if tipo == "player":
            self.player_menu(user)
        elif tipo == "club_member":
            self.club_menu(user)
        elif tipo == "referee":
            self.referee_menu(user)

    # ------------------------------
    # Menú Player
    # ------------------------------
    def player_menu(self, player: Player):
        while True:
            print("\n=== MENÚ JUGADOR ===")
            print("1. Ver estadísticas")
            print("2. Ver mi equipo")
            print("3. Ver historial de partidos")
            print("4. Actualizar perfil")
            print("5. Cerrar sesión")
            opcion = input("Selecciona: ")

            try:
                if opcion == "1":
                    print(self.player_service.view_stats(player))
                elif opcion == "2":
                    print("Equipo:", self.player_service.view_team(player))
                elif opcion == "3":
                    print(self.player_service.view_history(player))
                elif opcion == "4":
                    name = input("Nuevo nombre: ")
                    age = int(input("Nueva edad: "))
                    print(self.player_service.update_profile(player, name, age))
                elif opcion == "5":
                    self.auth_service.logout()
                    break
                else:
                    print("Opción inválida.")
            except ScoutingError as e:
                print("Error:", e)

    # ------------------------------
    # Menú ClubMember
    # ------------------------------
    def club_menu(self, member: ClubMember):
        while True:
            print("\n=== MENÚ CLUB MEMBER ===")
            print("1. Ver jugadores de mi equipo")
            print("2. Actualizar estadísticas de jugador")
            print("3. Crear reporte de partido")
            print("4. Ver mi perfil")
            print("5. Cerrar sesión")
            opcion = input("Selecciona: ")

            try:
                if opcion == "1":
                    jugadores = self.club_service.view_team_players(member, self.auth_service)
                    for j in jugadores:
                        print(f"- {j.get_name()} | {j.stats}")
                elif opcion == "2":
                    player_id = input("ID del jugador: ")
                    goles = int(input("Goles a sumar: "))
                    asistencias = int(input("Asistencias a sumar: "))
                    partidos = int(input("Partidos a sumar: "))
                    print(self.club_service.update_player_stats(member, self.auth_service, player_id, goles, asistencias, partidos))
                elif opcion == "3":
                    rival = input("Rival: ")
                    resultado = input("Resultado (ej: 2-1): ")
                    print(self.club_service.create_match_report(member, rival, resultado, self.auth_service))
                elif opcion == "4":
                    perfil = self.club_service.view_profile(member)
                    print(perfil)
                elif opcion == "5":
                    self.auth_service.logout()
                    break
                else:
                    print("Opción inválida.")
            except ScoutingError as e:
                print("Error:", e)

    # ------------------------------
    # Menú Referee
    # ------------------------------
    def referee_menu(self, referee: Referee):
        while True:
            print("\n=== MENÚ ÁRBITRO ===")
            print("1. Ver partidos asignados")
            print("2. Reportar resultado de partido")
            print("3. Ver mi perfil")
            print("4. Cerrar sesión")
            opcion = input("Selecciona: ")

            try:
                if opcion == "1":
                    print(self.referee_service.view_matches(referee))
                elif opcion == "2":
                    partido_id = input("ID del partido: ")
                    resultado = input("Resultado: ")
                    print(self.referee_service.report_result(referee, partido_id, resultado))
                elif opcion == "3":
                    perfil = self.referee_service.view_profile(referee)
                    print(perfil)
                elif opcion == "4":
                    self.auth_service.logout()
                    break
                else:
                    print("Opción inválida.")
            except ScoutingError as e:
                print("Error:", e)


# ==============================
# Ejecutar programa
# ==============================
if __name__ == "__main__":
    MenuSystem().main_menu()