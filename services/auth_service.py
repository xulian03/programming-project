from project import User, ClubMember, Player, Referee
from database.repository import RepositoryProvider

class AuthService:
    def __init__(self):
        self.current_user = None

    def register_player(self, id, password, name, age, team_id, position):
        if self.user_repo.find(id):
            raise ValueError("El usuario ya existe")
        
        if age <= 0:
            raise ValueError("Edad inválida")

        user = User(id, name, age)
        RepositoryProvider.get("User").save(user)
        return user

    def register_club_member(self, id, password, name, age, role):
        pass

    def register_referee(self, id, password, name, age, license):
        pass

    def login(self, id, password, user_type):
        pass

    def get_current_user():
        pass
    
    def logout():
        pass