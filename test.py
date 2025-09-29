from database.json_repository import JSONRepository
from database.repository import RepositoryProvider
from project import User, Player, Referee, Team, ClubMember, Position



def main():
    players_repo = JSONRepository(Player)
    club_members_repo = JSONRepository(ClubMember)
    teams_repo = JSONRepository(Team)
    referee_repo = JSONRepository(Referee)

    RepositoryProvider.register("Player", players_repo)
    RepositoryProvider.register("Team", teams_repo)
    RepositoryProvider.register("ClubMember", club_members_repo)
    RepositoryProvider.register("Referee", referee_repo)



    coach = ClubMember("c1", "Pep Guardiola", 52)
    team = Team("Barcelona", coach)
    player = Player("p1", "Messi", 36, 10, team, Position.DC)
    team.get_players().append(player)
    teams_repo.save(team)
    players_repo.save(player)
    club_members_repo.save(coach)

    for player in team.get_players():
        print(player.get_name())
    print(team.get_players())  # debería traer objetos Player
    print(player.get_team().get_name())  # debería traer "t1"


if __name__ == "__main__":
    main()