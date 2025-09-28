from database.json_repository import JSONRepository
from database.repository import RepositoryProvider
from project import User, Coach, Player, Team, Position



def main():
    players_repo = JSONRepository(Player)
    coachs_repo = JSONRepository(Coach)
    teams_repo = JSONRepository(Team)

    RepositoryProvider.register("Player", players_repo)
    RepositoryProvider.register("Team", teams_repo)
    RepositoryProvider.register("Coach", coachs_repo)


    repo_players = RepositoryProvider.get("Player")
    repo_teams = RepositoryProvider.get("Team")

    coach = Coach("c1", "Pep Guardiola", 52)
    team = Team("t1", coach)
    player = Player("p1", "Messi", 36, team, 10, Position.DC)
    team.get_players().append(player)
    repo_teams.save(team)
    repo_players.save(player)

    print(team.get_players())  # debería traer objetos Player
    print(player.get_team().get_id())  # debería traer "t1"


if __name__ == "__main__":
    main()