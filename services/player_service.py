from project import User, Player
from .auth_service import AuthService
from database.repository import RepositoryProvider

class PlayerManagementService:
    _instance = None

    def __init__(self):
        self.auth_service: AuthService = AuthService.get_instance()

    def get_player_stats(self, player_id=None):
        players_repo = self.auth_service.players_repo
        player: Player = players_repo.find(player_id)
        if player == None:
            return None
        return player.serialize()

    def update_player_profile(self, player_id=None, **updates):
        players_repo = self.auth_service.players_repo
        teams_repo = self.auth_service.teams_repo
        player: Player = players_repo.find(player_id) or self.auth_service.get_current_user()
        if not player:
            return False
        player.set_name(updates.get("name"))
        player.set_age(updates.get("age"))
        player.set_goals(updates.get("goals"))
        player.set_assists(updates.get("assists"))
        player.set_clearances(updates.get("clearences"))
        player.set_shots(updates.get("shots"))
        player.set_shots_on_target(updates.get("shots_on_target"))
        player.set_team(teams_repo.find(updates.get("team")))
        player.set_position(updates.get("position"))
        
        return True

    def get_all_players(self):
        pass

    def search_players(self, filters):
        pass

    def get_instance():
        if PlayerManagementService._instance is None:
            PlayerManagementService._instance = PlayerManagementService()
        return PlayerManagementService._instance