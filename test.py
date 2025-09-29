from database.json_repository import JSONRepository
from database.repository import RepositoryProvider
from project import User, Player, Referee, Team, ClubMember, Position
from services.auth_service import AuthService
from services.player_service import PlayerManagementService
from services.team_service import TeamService
from services.report_service import ReportService


def main():
    players_repo = JSONRepository(Player)
    club_members_repo = JSONRepository(ClubMember)
    teams_repo = JSONRepository(Team)
    referee_repo = JSONRepository(Referee)

    RepositoryProvider.register("Player", players_repo)
    RepositoryProvider.register("Team", teams_repo)
    RepositoryProvider.register("ClubMember", club_members_repo)
    RepositoryProvider.register("Referee", referee_repo)

    auth_service: AuthService = AuthService.get_instance()
    player_service: PlayerManagementService = PlayerManagementService.get_instance()
    team_service: TeamService = TeamService.get_instance()
    
    



if __name__ == "__main__":
    main()