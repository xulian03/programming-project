from database.json_repository import JSONRepository
from database.repository import RepositoryProvider
from project import User, Player, Referee, Team, ClubMember, Position
from services.auth_service import AuthService
from services.player_service import PlayerManagementService
from services.team_service import TeamService
from services.report_service import ReportService
from utils import title_style, default_text, separator, options, WIDTH


class MenuSystem:
    def __init__(self):
        self.auth_service: AuthService = AuthService.get_instance()
        self.player_service: PlayerManagementService = PlayerManagementService.get_instance()
        self.team_service: TeamService = TeamService.get_instance()
        self.report_service: ReportService = ReportService.get_instance()

    def main_menu(self):
        while True:
            print("\n" + separator())
            print(title_style("SISTEMA DE SCOUTING"))
            print(separator())
            
            try:
                opcion = options("Registrarse", "Iniciar sesión", "Salir", center=True)
                
                if opcion == "1":
                    self.register_flow()
                elif opcion == "2":
                    self.login_flow()
                elif opcion == "3":
                    print(default_text("Hasta luego"))
                    break
                else:
                    print(default_text("Opción inválida"))
            except Exception as e:
                print(default_text(f"Error: {e}"))
            except KeyboardInterrupt:
                if self.auth_service.logout():
                    print("\n" + default_text("Sesión cerrada"))
                print("\n" + default_text("Operación cancelada"))
                break

    def register_flow(self):
        print("\n" + separator())
        print(title_style("REGISTRO"))
        print(separator())
        
        print(default_text("Selecciona el tipo de usuario:"))
        tipo = options("Jugador", "Miembro del Club", "Árbitro", center=True)
        
        if tipo == "1":
            self.register_player()
        elif tipo == "2":
            self.register_club_member()
        elif tipo == "3":
            self.register_referee()
        else:
            print(default_text("Opción inválida"))

    def register_player(self):
        print("\n" + separator())
        print(title_style("REGISTRO DE JUGADOR"))
        print(separator())
        
        user_id = input("ID único: ".center(WIDTH)).strip()
        password = input("Contraseña (mín 6 caracteres): ".center(WIDTH)).strip()
        name = input("Nombre completo: ".center(WIDTH)).strip()
        age = input("Edad (16-45): ".center(WIDTH)).strip()
        team_id = input("ID del equipo (Enter para omitir): ".center(WIDTH)).strip() or None
        
        print("\n" + default_text("Posiciones disponibles:"))
        print(default_text("GK, LD, LI, DFC, MCD, MC, LW, MCO, DC, RW"))
        position = input("Posición: ".center(WIDTH)).strip().upper()
        
        try:
            age = int(age)
            player = self.auth_service.register_player(
                id=user_id,
                password=password,
                name=name,
                age=age,
                team_id=team_id,
                position=position
            )
            print("\n" + default_text(f"Jugador {name} registrado con éxito"))
            input(default_text("Presiona Enter para continuar..."))
            self.player_menu(player)
        except Exception as e:
            print("\n" + default_text(f"Error: {e}"))
            input(default_text("Presiona Enter para continuar..."))

    def register_club_member(self):
        print("\n" + separator())
        print(title_style("REGISTRO DE MIEMBRO DEL CLUB"))
        print(separator())
        
        user_id = input("ID único: ".center(WIDTH)).strip()
        password = input("Contraseña (mín 6 caracteres): ".center(WIDTH)).strip()
        name = input("Nombre completo: ".center(WIDTH)).strip()
        age = input("Edad (18-70): ".center(WIDTH)).strip()
        
        print("\n" + default_text("Roles disponibles:"))
        role = options("Coach", "Staff", "Manager", "Physio", center=True)
        
        role_map = {"1": "coach", "2": "staff", "3": "manager", "4": "physio"}
        role_str = role_map.get(role, "staff")
        
        try:
            age = int(age)
            member = self.auth_service.register_club_member(
                id=user_id,
                password=password,
                name=name,
                age=age,
                role=role_str
            )
            print("\n" + default_text(f"{role_str.capitalize()} {name} registrado con éxito"))
            input(default_text("Presiona Enter para continuar..."))
            self.club_member_menu(member)
        except Exception as e:
            print("\n" + default_text(f"Error: {e}"))
            input(default_text("Presiona Enter para continuar..."))

    def register_referee(self):
        print("\n" + separator())
        print(title_style("REGISTRO DE ÁRBITRO"))
        print(separator())
        
        user_id = input("ID único: ".center(WIDTH)).strip()
        password = input("Contraseña (mín 6 caracteres): ".center(WIDTH)).strip()
        name = input("Nombre completo: ".center(WIDTH)).strip()
        age = input("Edad (18-65): ".center(WIDTH)).strip()
        license = input("Número de licencia (único): ".center(WIDTH)).strip()
        
        try:
            age = int(age)
            referee = self.auth_service.register_referee(
                id=user_id,
                password=password,
                name=name,
                age=age,
                license=license
            )
            print("\n" + default_text(f"Árbitro {name} registrado con éxito"))
            input(default_text("Presiona Enter para continuar..."))
            self.referee_menu(referee)
        except Exception as e:
            print("\n" + default_text(f"Error: {e}"))
            input(default_text("Presiona Enter para continuar..."))

    def login_flow(self):
        print("\n" + separator())
        print(title_style("INICIAR SESIÓN"))
        print(separator())
        
        print(default_text("Selecciona el tipo de usuario:"))
        tipo = options("Jugador", "Miembro del Club", "Árbitro", center=True)
        
        tipo_map = {"1": "player", "2": "clubmember", "3": "referee"}
        user_type = tipo_map.get(tipo)
        
        if not user_type:
            print(default_text("Opción inválida"))
            return
        
        user_id = input("ID: ".center(WIDTH)).strip()
        password = input("Contraseña: ".center(WIDTH)).strip()
        
        try:
            success = self.auth_service.login(user_id, password, user_type)
            if not success:
                print("\n" + default_text("Credenciales incorrectas"))
                input(default_text("Presiona Enter para continuar..."))
                return
            
            user = self.auth_service.get_current_user()
            print("\n" + default_text(f"Bienvenido {user.get_name()}"))
            input(default_text("Presiona Enter para continuar..."))
            
            if user_type == "player":
                self.player_menu(user)
            elif user_type == "clubmember":
                self.club_member_menu(user)
            elif user_type == "referee":
                self.referee_menu(user)
        except Exception as e:
            print("\n" + default_text(f"Error: {e}"))
            input(default_text("Presiona Enter para continuar..."))

    def player_menu(self, player: Player):
        while True:
            print("\n" + separator())
            print(title_style(f"MENÚ JUGADOR - {player.get_name()}"))
            print(separator())
            
            try:
                opcion = options(
                    "Ver mis estadísticas",
                    "Ver mi equipo",
                    "Actualizar mi perfil",
                    "Cerrar sesión",
                    center=True
                )
                
                if opcion == "1":
                    self.view_player_stats()
                elif opcion == "2":
                    self.view_player_team(player)
                elif opcion == "3":
                    self.update_player_profile(player)
                elif opcion == "4":
                    self.auth_service.logout()
                    print(default_text("Sesión cerrada"))
                    break
                else:
                    print(default_text("Opción inválida"))
            except Exception as e:
                print(default_text(f"Error: {e}"))
                input(default_text("Presiona Enter para continuar..."))

    def view_player_stats(self, player: Player=None):
        try:
            stats = self.player_service.get_player_stats(player)
            print("\n" + separator())
            print(title_style("MIS ESTADÍSTICAS"))
            print(separator())
            print(default_text(f"Nombre: {stats.get('_name', 'N/A')}"))
            print(default_text(f"Edad: {stats.get('_age', 'N/A')}"))
            print(default_text(f"Posición: {stats.get('_position', 'N/A')}"))
            print(default_text(f"Goles: {stats.get('_goals', 0)}"))
            print(default_text(f"Asistencias: {stats.get('_assists', 0)}"))
            print(default_text(f"Tiros: {stats.get('_shots', 0)}"))
            print(default_text(f"Tiros a puerta: {stats.get('_shots_on_target', 0)}"))
            print(default_text(f"Despejes: {stats.get('_clearances', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error al obtener estadísticas: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def view_player_team(self, player: Player):
        try:
            team = player.get_team()
            if not team:
                print(default_text("No tienes equipo asignado"))
                input(default_text("Presiona Enter para continuar..."))
                return
            
            print("\n" + separator())
            print(title_style("MI EQUIPO"))
            print(separator())
            print(default_text(f"Nombre: {team.get_name()}"))
            
            # Obtener jugadores del equipo
            all_players = self.player_service.get_all_players(team.get_id())
            print("\n" + default_text("Compañeros de equipo:"))
            for teammate in all_players:
                if teammate.get('_id') != player.get_id():
                    print(default_text(f"- {teammate.get('_name')} ({teammate.get('_position')})"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error al obtener información del equipo: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def update_player_profile(self, player: Player):
        print("\n" + separator())
        print(title_style("ACTUALIZAR PERFIL"))
        print(separator())
        
        name = input("Nuevo nombre (Enter para mantener): ".center(WIDTH)).strip()
        age = input("Nueva edad (Enter para mantener): ".center(WIDTH)).strip()
        
        updates = {}
        if name:
            updates['name'] = name
        if age:
            try:
                updates['age'] = int(age)
            except ValueError:
                print(default_text("Error: Edad debe ser un número"))
                input(default_text("Presiona Enter para continuar..."))
                return
        
        
        if updates:
            try:
                self.player_service.update_player_profile(**updates)
                print(default_text("Perfil actualizado con éxito"))
                # Actualizar el objeto player local
                if name:
                    player.set_name(name)
                if age:
                    player.set_age(int(age))
            except Exception as e:
                print(default_text(f"Error al actualizar: {e}"))
        else:
            print(default_text("No se realizaron cambios"))
        input(default_text("Presiona Enter para continuar..."))

    def club_member_menu(self, member: ClubMember):
        while True:
            print("\n" + separator())
            print(title_style(f"MENÚ {member.get_role().upper()} - {member.get_name()}"))
            print(separator())
            
            try:
                menu_options = ["Ver mi perfil"]
                if not member.get_team():
                    if member.get_role() == "coach":
                        menu_options.append("Crear equipo")
                else:
                    menu_options.extend([
                        "Ver jugadores de mi equipo",
                        "Gestionar mi equipo"
                    ])
                
                menu_options.extend(["Ver estadísticas de jugador específico", "Cerrar sesión"])
                
                opcion = options(*menu_options, center=True)
                
                if opcion == "1":
                    self.view_club_member_profile(member)
                elif member.get_role() == "coach" and not member.get_team() and opcion == "2":
                    self.create_team(member)
                elif member.get_team() and opcion == "2":
                    self.view_team_players(member)
                elif member.get_team() and opcion == "3":
                    self.manage_team(member)
                elif opcion == str(len(menu_options) - 1):
                    self.view_specific_player_stats()
                elif opcion == str(len(menu_options)):
                    self.auth_service.logout()
                    print(default_text("Sesión cerrada"))
                    break
                else:
                    print(default_text("Opción inválida"))
            except Exception as e:
                print(default_text(f"Error: {e}"))
                input(default_text("Presiona Enter para continuar..."))

    def view_team_players(self, member: ClubMember):
        if not member.get_team():
            print(default_text("No tienes equipo asignado"))
            input(default_text("Presiona Enter para continuar..."))
            return
        try:
            players = self.player_service.get_all_players()
            if len(players):
                print(default_text("El equipo no tiene jugadores."))
                input(default_text("Presiona Enter para continuar..."))
                return
            print("\n" + separator())
            print(title_style(f"JUGADORES DEL {member.get_team().get_name().capitalize()}"))
            print(separator())
            for player in players:
                print(default_text(f"{player.get('_name')} - {player.get('_position')}"))
                print(default_text(f"  Goles: {player.get('_goals', 0)} | Asistencias: {player.get('_assists', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def view_specific_player_stats(self):
    
        player_id = input("ID del jugador: ".center(WIDTH)).strip()
        
        try:
            stats = self.player_service.get_player_stats(player_id)
            print("\n" + separator())
            print(title_style(f"ESTADÍSTICAS DE {stats.get('_name', 'N/A')}"))
            print(separator())
            print(default_text(f"Posición: {stats.get('_position', 'N/A')}"))
            print(default_text(f"Edad: {stats.get('_age', 'N/A')}"))
            print(default_text(f"Goles: {stats.get('_goals', 0)}"))
            print(default_text(f"Asistencias: {stats.get('_assists', 0)}"))
            print(default_text(f"Tiros: {stats.get('_shots', 0)}"))
            print(default_text(f"Tiros a puerta: {stats.get('_shots_on_target', 0)}"))
            print(default_text(f"Despejes: {stats.get('_clearances', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def manage_team(self, member: ClubMember):
        if not member.get_team() or member.get_role() != "coach":
            print(default_text("Solo los entrenadores con equipo pueden gestionar"))
            input(default_text("Presiona Enter para continuar..."))
            return
        
        print("\n" + separator())
        print(title_style("GESTIONAR EQUIPO"))
        print(separator())
        
        opcion = options("Agregar jugador", "Remover jugador", "Volver", center=True)
        
        try:
            team_id = member.get_team().get_id()
            
            if opcion == "1":
                player_id = input("ID del jugador a agregar: ".center(WIDTH)).strip()
                success = self.team_service.add_player_to_team(team_id, player_id)
                if success:
                    print(default_text("Jugador agregado con éxito"))
                else:
                    print(default_text("No se pudo agregar el jugador"))
            elif opcion == "2":
                player_id = input("ID del jugador a remover: ".center(WIDTH)).strip()
                success = self.team_service.remove_player_to_team(team_id, player_id)
                if success:
                    print(default_text("Jugador removido con éxito"))
                else:
                    print(default_text("No se pudo remover el jugador"))
        except Exception as e:
            print(default_text(f"Error: {e}"))
        
        input(default_text("Presiona Enter para continuar..."))

    def create_team(self, member):
        print("\n" + separator())
        print(title_style("CREAR EQUIPO"))
        print(separator())
        
        team_id = input("ID del equipo: ".center(WIDTH)).strip()
        team_name = input("Nombre del equipo: ".center(WIDTH)).strip()
        
        try:
            team = self.team_service.create_team(team_id, team_name)
            # Asignar el equipo al coach
            member.set_team(team)
            self.auth_service.club_members_repo.replace(member.get_id(), member)
            print(default_text(f"Equipo {team_name} creado con éxito"))
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def view_club_member_profile(self, member: ClubMember):
        print("\n" + separator())
        print(title_style("MI PERFIL"))
        print(separator())
        print(default_text(f"ID: {member.get_id()}"))
        print(default_text(f"Nombre: {member.get_name()}"))
        print(default_text(f"Edad: {member.get_age()}"))
        print(default_text(f"Rol: {member.get_role()}"))
        team = member.get_team()
        team_display = "Sin equipo"
        if team:
            team_display = team.get_id() if hasattr(team, 'get_id') else team.get('id', 'Sin equipo')
        print(default_text(f"Equipo: {team_display}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))

    def referee_menu(self, referee: Referee):
        while True:
            print("\n" + separator())
            print(title_style(f"MENÚ ÁRBITRO - {referee.get_name()}"))
            print(separator())
            
            try:
                opcion = options(
                    "Ver estadísticas de cualquier jugador",
                    "Ver información de cualquier equipo",
                    "Ver todos los jugadores",
                    "Buscar jugadores con filtros",
                    "Ver mi perfil",
                    "Cerrar sesión",
                    center=True
                )
                
                if opcion == "1":
                    self.view_any_player_stats()
                elif opcion == "2":
                    self.view_any_team_info()
                elif opcion == "3":
                    self.view_all_players()
                elif opcion == "4":
                    self.search_players_with_filters()
                elif opcion == "5":
                    self.view_referee_profile(referee)
                elif opcion == "6":
                    self.auth_service.logout()
                    print(default_text("Sesión cerrada"))
                    break
                else:
                    print(default_text("Opción inválida"))
            except Exception as e:
                print(default_text(f"Error: {e}"))
                input(default_text("Presiona Enter para continuar..."))

    def view_any_player_stats(self):
        player_id = input("ID del jugador: ".center(WIDTH)).strip()
        
        try:
            stats = self.player_service.get_player_stats(player_id)
            print(stats)
            print("\n" + separator())
            print(title_style(f"ESTADÍSTICAS DE {stats.get('_name', 'N/A')}"))
            print(separator())
            print(default_text(f"Edad: {stats.get('_age', 'N/A')}"))
            print(default_text(f"Posición: {stats.get('_position', 'N/A')}"))
            print(default_text(f"Goles: {stats.get('_goals', 0)}"))
            print(default_text(f"Asistencias: {stats.get('_assists', 0)}"))
            print(default_text(f"Tiros: {stats.get('_shots', 0)}"))
            print(default_text(f"Tiros a puerta: {stats.get('_shots_on_target', 0)}"))
            print(default_text(f"Despejes: {stats.get('_clearances', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def view_any_team_info(self):
        team_id = input("ID del equipo: ".center(WIDTH)).strip()
        
        try:
            team_info: Team = self.team_service.get_team_info(team_id)
            if not team_info:
                print(default_text("Equipo no encontrado"))
                input(default_text("Presiona Enter para continuar..."))
                return
            
            print("\n" + separator())
            print(title_style(f"EQUIPO: {team_info.get_name()}"))
            print(separator())
            
            # Obtener jugadores del equipo
            players = self.player_service.get_all_players(team_id)
            print("\n" + default_text("Jugadores:"))
            for player in players:
                print(default_text(f"- {player.get('_name')} ({player.get('_position')})"))
                print(default_text(f"  Goles: {player.get('_goals', 0)} | Asistencias: {player.get('_assists', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def view_all_players(self):
        try:
            players = self.player_service.get_all_players()
            print("\n" + separator())
            print(title_style("TODOS LOS JUGADORES"))
            print(separator())
            for player in players:
                print(default_text(f"{player.get('_name')} - {player.get('_position')}"))
                print(default_text(f"  G: {player.get('_goals', 0)} | A: {player.get('_assists', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def search_players_with_filters(self):
        print("\n" + separator())
        print(title_style("BUSCAR JUGADORES"))
        print(separator())
        
        print(default_text("Filtros opcionales (Enter para omitir):"))
        position = input("Posición: ".center(WIDTH)).strip().upper() or None
        
        
        try:
            filters = {}
            if position:
                filters['_position'] = Position(position)
            players = self.player_service.search_players(filters)
            
            print("\n" + separator())
            print(title_style("RESULTADOS"))
            print(separator())
            for player in players:
                print(default_text(f"{player.get('_name')} - {player.get('_position')}"))
                print(default_text(f"  G: {player.get('_goals', 0)} | A: {player.get('_assists', 0)}"))
            print(separator())
        except Exception as e:
            print(default_text(f"Error: {e}"))
        input(default_text("Presiona Enter para continuar..."))

    def view_referee_profile(self, referee: Referee):
        print("\n" + separator())
        print(title_style("MI PERFIL"))
        print(separator())
        print(default_text(f"ID: {referee.get_id()}"))
        print(default_text(f"Nombre: {referee.get_name()}"))
        print(default_text(f"Edad: {referee.get_age()}"))
        print(default_text(f"Licencia: {referee.get_license()}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))


def main():
    players_repo = JSONRepository(Player)
    club_members_repo = JSONRepository(ClubMember)
    teams_repo = JSONRepository(Team)
    referee_repo = JSONRepository(Referee)

    RepositoryProvider.register("Player", players_repo)
    RepositoryProvider.register("Team", teams_repo)
    RepositoryProvider.register("ClubMember", club_members_repo)
    RepositoryProvider.register("Referee", referee_repo)

    menu_system = MenuSystem()
    menu_system.main_menu()


if __name__ == "__main__":
    main()