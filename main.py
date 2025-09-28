import utils
import authenticator


print(utils.separator())
print(utils.title_style("BIENVENIDO/A A %NOMBRE-APP%"))
print(utils.separator())
print()
authenticator.auth()

# =============================
# 📌 AUTENTICACIÓN
# =============================
class AuthSystem:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def register(self, user_type):
        user_id = input("ID: ")
        password = input("Password: ")
        name = input("Name: ")
        age = int(input("Age: "))

        if user_type == "player":
            team_id = input("Team ID: ")
            squad_num = input("Squad Number: ")
            position = input("Position: ")
            user = Player(user_id, password, name, age, team_id, squad_num, position)

        elif user_type == "clubmember":
            role = input("Role: ")
            team_coach = input("Team Coach: ")
            user = ClubMember(user_id, password, name, age, role, team_coach)

        elif user_type == "referee":
            licencia = input("Licencia: ")
            user = Referee(user_id, password, name, age, licencia)

        else:
            print("Tipo de usuario inválido.")
            return

        self.users[user_id] = user
        print(f"✅ {user_type.capitalize()} registrado con éxito!")

    def login(self):
        user_id = input("ID: ")
        password = input("Password: ")

        user = self.users.get(user_id)
        if user and user.password == password:
            self.current_user = user
            print(f"✅ Bienvenido {user.name} ({type(user).__name__})")
        else:
            print("❌ Credenciales inválidas.")


# =============================
# 📌 MENÚS SEGÚN USUARIO
# =============================
class PlayerMenu:
    def show(self, user):
        while True:
            print("\n--- MENÚ JUGADOR ---")
            print("1. Ver mis estadísticas")
            print("2. Ver mi equipo")
            print("3. Ver mi historial de partidos")
            print("4. Actualizar mi perfil")
            print("5. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            match opcion:
                case "1": print("📊 Mostrando estadísticas...")
                case "2": print("⚽ Mostrando equipo...")
                case "3": print("📜 Mostrando historial...")
                case "4": print("✏️ Actualizando perfil...")
                case "5": break
                case _: print("Opción inválida.")


class ClubMemberMenu:
    def show(self, user):
        while True:
            print("\n--- MENÚ CLUB MEMBER ---")
            print("1. Ver jugadores de mi equipo")
            print("2. Actualizar estadísticas de jugador")
            print("3. Crear reporte de partido")
            print("4. Gestionar planilla del equipo")
            print("5. Ver mi perfil")
            print("6. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            match opcion:
                case "1": print("👥 Jugadores del equipo...")
                case "2": print("📊 Actualizando estadísticas...")
                case "3": print("📝 Creando reporte...")
                case "4": print("📋 Gestionando planilla...")
                case "5": print("🙍 Ver perfil...")
                case "6": break
                case _: print("Opción inválida.")


class RefereeMenu:
    def show(self, user):
        while True:
            print("\n--- MENÚ ÁRBITRO ---")
            print("1. Validar estadísticas de partido")
            print("2. Crear registro oficial de partido")
            print("3. Ver partidos asignados")
            print("4. Ver mi perfil")
            print("5. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            match opcion:
                case "1": print("✅ Validando estadísticas...")
                case "2": print("📝 Creando registro oficial...")
                case "3": print("📅 Mostrando partidos asignados...")
                case "4": print("🙍 Ver perfil árbitro...")
                case "5": break
                case _: print("Opción inválida.")


# =============================
# 📌 MENÚ PRINCIPAL
# =============================
class MainMenu:
    def __init__(self):
        self.auth = AuthSystem()
        self.player_menu = PlayerMenu()
        self.club_menu = ClubMemberMenu()
        self.referee_menu = RefereeMenu()

    def show(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Seleccionar tipo de usuario y registrarse")
            print("2. Iniciar sesión")
            print("3. Menú según usuario logueado")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")
            match opcion:
                case "1":
                    print("1. Player\n2. Club Member\n3. Referee")
                    tipo = input("Seleccione tipo de usuario: ")
                    tipos = {"1": "player", "2": "clubmember", "3": "referee"}
                    self.auth.register(tipos.get(tipo, ""))
                case "2":
                    self.auth.login()
                case "3":
                    if not self.auth.current_user:
                        print("❌ Debes iniciar sesión primero.")
                        continue
                    user = self.auth.current_user
                    if isinstance(user, Player): self.player_menu.show(user)
                    elif isinstance(user, ClubMember): self.club_menu.show(user)
                    elif isinstance(user, Referee): self.referee_menu.show(user)
                case "4":
                    print("👋 Saliendo del programa...")
                    break
                case _:
                    print("Opción inválida.")
    