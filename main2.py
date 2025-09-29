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
        self.auth_service = AuthService.get_instance()
        self.player_service = PlayerManagementService.get_instance()
        self.team_service = TeamService.get_instance()
        self.report_service = ReportService.get_instance()

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
        team_id = input("ID del equipo: ".center(WIDTH)).strip()
        
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
        
        extra_fields = {}
        if role_str == "coach":
            years_exp = input("Años de experiencia: ".center(WIDTH)).strip()
            specialization = input("Especialización: ".center(WIDTH)).strip()
            try:
                extra_fields["years_experience"] = int(years_exp)
                extra_fields["specialization"] = specialization
            except ValueError:
                print(default_text("Error: Años de experiencia debe ser un número"))
                return
        
        try:
            age = int(age)
            member = self.auth_service.register_club_member(
                id=user_id,
                password=password,
                name=name,
                age=age,
                role=role_str,
                **extra_fields
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
        
        tipo_map = {"1": "player", "2": "club_member", "3": "referee"}
        user_type = tipo_map.get(tipo)
        
        if not user_type:
            print(default_text("Opción inválida"))
            return
        
        user_id = input("ID: ".center(WIDTH)).strip()
        password = input("Contraseña: ".center(WIDTH)).strip()
        
        try:
            user = self.auth_service.login(user_id, password, user_type)
            print("\n" + default_text(f"Bienvenido {user.get_name()}"))
            input(default_text("Presiona Enter para continuar..."))
            
            if user_type == "player":
                self.player_menu(user)
            elif user_type == "club_member":
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
                    self.view_player_stats(player)
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

    def view_player_stats(self, player: Player):
        stats = self.player_service.get_player_stats()
        print("\n" + separator())
        print(title_style("MIS ESTADÍSTICAS"))
        print(separator())
        print(default_text(f"Goles: {stats['goals']}"))
        print(default_text(f"Asistencias: {stats['assists']}"))
        print(default_text(f"Tiros: {stats['shots']}"))
        print(default_text(f"Tiros a puerta: {stats['shots_on_target']}"))
        print(default_text(f"Despejes: {stats['clearances']}"))
        print(default_text(f"Partidos jugados: {stats['matches_played']}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))

    def view_player_team(self, player: Player):
        team_info = self.team_service.get_team_info()
        print("\n" + separator())
        print(title_style("MI EQUIPO"))
        print(separator())
        print(default_text(f"Nombre: {team_info['name']}"))
        print(default_text(f"Entrenador: {team_info['coach_name']}"))
        print("\n" + default_text("Compañeros de equipo:"))
        for teammate in team_info['players']:
            if teammate['id'] != player.get_id():
                print(default_text(f"- {teammate['name']} ({teammate['position']})"))
        print(separator())
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
                return
        
        if updates:
            self.player_service.update_player_profile(player.get_id(), **updates)
            print(default_text("Perfil actualizado con éxito"))
        else:
            print(default_text("No se realizaron cambios"))
        input(default_text("Presiona Enter para continuar..."))

    def club_member_menu(self, member: ClubMember):
        while True:
            print("\n" + separator())
            print(title_style(f"MENÚ {member.get_role().upper()} - {member.get_name()}"))
            print(separator())
            
            try:
                menu_options = [
                    "Ver jugadores de mi equipo",
                    "Ver estadísticas de jugador específico",
                    "Gestionar mi equipo"
                ]
                
                if member.get_role() == "coach" and not member.get_team():
                    menu_options.append("Crear equipo")
                
                menu_options.extend(["Ver mi perfil", "Cerrar sesión"])
                
                opcion = options(*menu_options, center=True)
                
                if opcion == "1":
                    self.view_team_players(member)
                elif opcion == "2":
                    self.view_specific_player_stats(member)
                elif opcion == "3":
                    self.manage_team(member)
                elif opcion == "4" and member.get_role() == "coach" and not member.get_team():
                    self.create_team(member)
                elif opcion == str(len(menu_options) - 1):
                    self.view_club_member_profile(member)
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
        
        team_info = self.team_service.get_team_info()
        print("\n" + separator())
        print(title_style("JUGADORES DEL EQUIPO"))
        print(separator())
        for player in team_info['players']:
            print(default_text(f"{player['name']} - {player['position']}"))
            print(default_text(f"  Goles: {player['goals']} | Asistencias: {player['assists']}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))

    def view_specific_player_stats(self, member: ClubMember):
        if not member.get_team():
            print(default_text("No tienes equipo asignado"))
            input(default_text("Presiona Enter para continuar..."))
            return
        
        player_id = input("ID del jugador: ".center(WIDTH)).strip()
        stats = self.player_service.get_player_stats(player_id)
        
        print("\n" + separator())
        print(title_style(f"ESTADÍSTICAS DE {stats['name']}"))
        print(separator())
        print(default_text(f"Posición: {stats['position']}"))
        print(default_text(f"Goles: {stats['goals']}"))
        print(default_text(f"Asistencias: {stats['assists']}"))
        print(default_text(f"Tiros: {stats['shots']}"))
        print(default_text(f"Tiros a puerta: {stats['shots_on_target']}"))
        print(default_text(f"Despejes: {stats['clearances']}"))
        print(default_text(f"Partidos jugados: {stats['matches_played']}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))

    def manage_team(self, member: ClubMember):
        if not member.get_team() or member.get_role() != "coach":
            print(default_text("Solo los entrenadores con equipo pueden gestionar"))
            input(default_text("Presiona Enter para continuar..."))
            return
        
        print("\n" + separator())
        print(title_style("GESTIONAR EQUIPO"))
        print(separator())
        
        opcion = options("Agregar jugador", "Remover jugador", "Cambiar nombre del equipo", "Volver", center=True)
        
        if opcion == "1":
            player_id = input("ID del jugador a agregar: ".center(WIDTH)).strip()
            self.team_service.add_player_to_team(member.get_team(), player_id)
            print(default_text("Jugador agregado con éxito"))
        elif opcion == "2":
            player_id = input("ID del jugador a remover: ".center(WIDTH)).strip()
            self.team_service.remove_player_from_team(member.get_team(), player_id)
            print(default_text("Jugador removido con éxito"))
        elif opcion == "3":
            new_name = input("Nuevo nombre del equipo: ".center(WIDTH)).strip()
            team = RepositoryProvider.get("Team").find(member.get_team())
            team.set_name(new_name)
            RepositoryProvider.get("Team").replace(team)
            print(default_text("Nombre actualizado con éxito"))
        
        input(default_text("Presiona Enter para continuar..."))

    def create_team(self, member):
        print("\n" + separator())
        print(title_style("CREAR EQUIPO"))
        print(separator())
        
        team_id = input("ID del equipo: ".center(WIDTH)).strip()
        team_name = input("Nombre del equipo: ".center(WIDTH)).strip()
        
        self.team_service.create_team(team_id, team_name, member.get_id())
        print(default_text(f"Equipo {team_name} creado con éxito"))
        input(default_text("Presiona Enter para continuar..."))

    def view_club_member_profile(self, member: ClubMember):
        print("\n" + separator())
        print(title_style("MI PERFIL"))
        print(separator())
        print(default_text(f"ID: {member.get_id()}"))
        print(default_text(f"Nombre: {member.get_name()}"))
        print(default_text(f"Edad: {member.get_age()}"))
        print(default_text(f"Rol: {member.get_role()}"))
        print(default_text(f"Equipo: {member.get_team() or 'Sin equipo'}"))

        
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
                    "Generar reporte de todos los jugadores",
                    "Ver mi perfil",
                    "Cerrar sesión",
                    center=True
                )
                
                if opcion == "1":
                    self.view_any_player_stats()
                elif opcion == "2":
                    self.view_any_team_info()
                elif opcion == "3":
                    self.generate_full_report()
                elif opcion == "4":
                    self.view_referee_profile(referee)
                elif opcion == "5":
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
        stats = self.player_service.get_player_stats(player_id)
        
        print("\n" + separator())
        print(title_style(f"ESTADÍSTICAS DE {stats['name']}"))
        print(separator())
        print(default_text(f"Edad: {stats['age']}"))
        print(default_text(f"Equipo: {stats['team_name']}"))
        print(default_text(f"Posición: {stats['position']}"))
        print(default_text(f"Goles: {stats['goals']}"))
        print(default_text(f"Asistencias: {stats['assists']}"))
        print(default_text(f"Tiros: {stats['shots']}"))
        print(default_text(f"Tiros a puerta: {stats['shots_on_target']}"))
        print(default_text(f"Despejes: {stats['clearances']}"))
        print(default_text(f"Partidos jugados: {stats['matches_played']}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))

    def view_any_team_info(self):
        team_id = input("ID del equipo: ".center(WIDTH)).strip()
        team_info = self.team_service.get_team_info(team_id)
        
        print("\n" + separator())
        print(title_style(f"EQUIPO: {team_info['name']}"))
        print(separator())
        print(default_text(f"Entrenador: {team_info['coach_name']}"))
        print("\n" + default_text("Jugadores:"))
        for player in team_info['players']:
            print(default_text(f"- {player['name']} ({player['position']})"))
            print(default_text(f"  Goles: {player['goals']} | Asistencias: {player['assists']}"))
        print(separator())
        input(default_text("Presiona Enter para continuar..."))

    def generate_full_report(self):
        print("\n" + separator())
        print(title_style("GENERAR REPORTE"))
        print(separator())
        
        print(default_text("Filtros opcionales (Enter para omitir):"))
        position = input("Posición: ".center(WIDTH)).strip().upper() or None
        age_min = input("Edad mínima: ".center(WIDTH)).strip()
        age_max = input("Edad máxima: ".center(WIDTH)).strip()
        team_id = input("ID del equipo: ".center(WIDTH)).strip() or None
        
        filters = {}
        if position:
            filters['position'] = position
        if age_min:
            filters['age_min'] = int(age_min)
        if age_max:
            filters['age_max'] = int(age_max)
        if team_id:
            filters['team_id'] = team_id
        
        report = self.report_service.generate_player_report(filters)
        
        print("\n" + separator())
        print(title_style("REPORTE DE JUGADORES"))
        print(separator())
        for player_data in report:
            print(default_text(f"{player_data['name']} - {player_data['position']} ({player_data['team_name']})"))
            print(default_text(f"  G: {player_data['goals']} | A: {player_data['assists']} | P: {player_data['matches_played']}"))
        print(separator())
        
        export = input("¿Exportar a CSV? (s/n): ".center(WIDTH)).strip().lower()
        if export == 's':
            filename = input("Nombre del archivo: ".center(WIDTH)).strip()
            self.report_service.export_to_csv(report, filename)
            print(default_text(f"Reporte exportado a {filename}.csv"))
        
        input(default_text("Presiona Enter para continuar..."))

    def view_referee_profile(self, referee: Referee):
        print("\n" + separator())
        print(title_style("MI PERFIL"))
        print(separator())
        print(default_text(f"ID: {referee.get_id()}"))
        print(default_text(f"Nombre: {referee.get_name()}"))
        print(default_text(f"Edad: {referee.get_age()}"))
        print(default_text(f"Licencia: {referee.get_license()}"))
        print(default_text(f"Partidos oficiados: {referee.get_matches_officiated()}"))
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