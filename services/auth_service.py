from project import User, ClubMember, Player, Referee
from database.repository import RepositoryProvider

class AuthService:
    _instance = None

    def __init__(self):
        self.players_repo = RepositoryProvider.get("Player")
        self.club_members_repo = RepositoryProvider.get("ClubMember")
        self.referee_repo = RepositoryProvider.get("Referee")
        self.teams_repo = RepositoryProvider.get("Team")
        self._current_user = None

    def register_player(self, id, name, age, password, team_id, position):
        if self._current_user:
            return None
        if self.players_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        team = self.teams_repo.find(team_id) if team_id != None else None
        player = Player(id, name, age, password, team, position)
        self.players_repo.save(player)
        self._current_user = player
        return player

    def register_club_member(self, id, password, name, age, role: str):
        if self._current_user:
            return None
        
        if self.club_members_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        club_member = ClubMember(id, name, age, password, None, role.lower())
        self.club_members_repo.save(club_member)
        self._current_user = club_member
        return club_member

    def register_referee(self, id, password, name, age, license):
        if self._current_user:
            return None
        
        if self.referee_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        ref = Referee(id, name, age, password, license)
        self.referee_repo.save(ref)
        self._current_user = ref
        return ref

    def login(self, id, password, user_type: str):
        if self._current_user:
            return False
        user: User = None
        match user_type.lower():
            case "player":
                user = self.players_repo.find(id)
            case "clubmember":
                user = self.club_members_repo.find(id)
            case "referee":
                user = self.referee_repo.find(id)
            case _:
                return False
        if not user:
            return False
        if user.verify_password(password):
            self._current_user = user
            return True


    def get_current_user(self):
        return self._current_user
    
    def set_current_user(self, user):
        self._current_user = user

    def logout(self):
        if self._current_user:
            self.players_repo.save(self._current_user)
            self._current_user = None

    def get_instance():
        if AuthService._instance is None:
            AuthService._instance = AuthService()
        return AuthService._instance