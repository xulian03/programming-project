from project import User, ClubMember, Player, Referee
from database.repository import RepositoryProvider

class AuthService:
    def __init__(self):
        self.users_repo = RepositoryProvider.get("User")
        self.club_members_repo = RepositoryProvider.get("ClubMember")
        self.referee_repo = RepositoryProvider.get("Referee")
        self.current_user = None

    def register_player(self, id, password, name, age, team_id, position):
        if self.users_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        teams_repo = RepositoryProvider.get("teams")
        team = teams_repo.find(team_id) if team_id != None else None
        player = Player(id, name, password, age, team, position)
        self.users_repo.save(player)
        self.current_user = player
        return player

    def register_club_member(self, id, password, name, age, role: str):
        if self.club_members_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        club_member = ClubMember(id, name, age, password, None, role.lower())
        self.club_members_repo.save(club_member)
        self.current_user = club_member
        return club_member

    def register_referee(self, id, password, name, age, license):
        if self.referee_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        ref = Referee(id, name, age, password, license)
        self.referee_repo.save(ref)
        self.current_user = ref
        return ref

    def login(self, id, password, user_type: str):
        user: User = None
        match user_type.lower():
            case "player":
                user = self.users_repo.find(id)
            case "clubmember":
                user = self.club_members_repo.find(id)
            case "referee":
                user = self.referee_repo.find(id)
            case _:
                return
        user.verify_password(password)


    def get_current_user(self):
        return self.current_user
    
    def logout(self):
        self.current_user = None