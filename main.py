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