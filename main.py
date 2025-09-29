import time


# -------------------------------
# Menú principal
# -------------------------------
class MainMenu:
    """
    Clase que gestiona el menú principal del sistema.
    Permite registrar usuarios, iniciar sesión y salir.
    """

    def __init__(self):
        # Lista donde se almacenan todos los usuarios registrados
        self.users = []

    def show(self):
        """
        Muestra el menú principal en un bucle infinito hasta que el usuario decida salir.
        """
        while True:
            print("=== MENÚ PRINCIPAL ===")
            print("1. Registrarse")
            print("2. Iniciar sesión")
            print("3. Salir")
            option = input("Selecciona: ")

            if option == "1":
                self.register_user()
            elif option == "2":
                self.login()
            elif option == "3":
                print("Saliendo del sistema...")
                time.sleep(2)
                break
            else:
                print("Opción inválida")
                time.sleep(2)

    def register_user(self):
        """
        Permite registrar un nuevo usuario del tipo:
        - Jugador
        - Staff (Miembro del club)
        - Árbitro
        Incluye validaciones de edad y longitud de contraseña.
        """
        print("=== REGISTRO ===")
        print("1. Jugador")
        print("2. Staff")
        print("3. Árbitro")
        user_type = input("Selecciona el tipo de usuario: ")

        id = input("ID: ")
        name = input("Nombre: ")
        age = int(input("Edad: "))
        password = input("Contraseña: ")

        # Validación de longitud de contraseña
        if len(password) < 6:
            print("La contraseña debe tener mínimo 6 caracteres")
            time.sleep(2)
            return

        # Registro de Jugador
        if user_type == "1":
            if age < 14 or age > 62:
                print("Edad inválida para jugador")
                time.sleep(2)
                return
            position = input("Posición: ")
            team = input("Equipo: ")
            player = Player(id, name, age, password, position, team)
            self.users.append(player)
            print("Jugador registrado con éxito")
            time.sleep(2)

        # Registro de Staff
        elif user_type == "2":
            if age < 18:
                print("Edad inválida para staff")
                time.sleep(2)
                return
            team = input("Equipo: ")
            role = input("Rol: ")
            staff = ClubMember(id, name, age, password, team, role)
            self.users.append(staff)
            print("Staff registrado con éxito")
            time.sleep(2)

        # Registro de Árbitro
        elif user_type == "3":
            if age < 18 or age > 62:
                print("Edad inválida para árbitro")
                time.sleep(2)
                return
            license = input("Licencia: ")
            referee = Referee(id, name, age, password, license)
            self.users.append(referee)
            print("Árbitro registrado con éxito")
            time.sleep(2)

        else:
            print("Tipo de usuario inválido")
            time.sleep(2)

    def login(self):
        """
        Permite iniciar sesión validando ID y contraseña.
        Dependiendo del tipo de usuario, abre el menú correspondiente.
        """
        print("=== INICIO DE SESIÓN ===")
        id = input("ID: ")
        password = input("Contraseña: ")

        # Busca un usuario que coincida con las credenciales
        user = next((u for u in self.users if u.id == id and u.check_password(password)), None)

        if user:
            print("Inicio de sesión exitoso")
            time.sleep(2)
            # Redirigir al menú correspondiente
            if isinstance(user, Player):
                PlayerMenu(user).show()
            elif isinstance(user, ClubMember):
                StaffMenu(user).show()
            elif isinstance(user, Referee):
                RefereeMenu(user).show()
        else:
            print("Credenciales incorrectas")
            time.sleep(2)


# -------------------------------
# Menú de Jugador
# -------------------------------
class PlayerMenu:
    """
    Menú específico para jugadores.
    Permite ver estadísticas, actualizar perfil y cerrar sesión.
    """

    def __init__(self, player):
        self.player = player

    def show(self):
        """
        Muestra el menú del jugador en un bucle.
        """
        while True:
            print("=== MENÚ JUGADOR ===")
            print("1. Ver estadísticas")
            print("2. Actualizar perfil")
            print("3. Cerrar sesión")
            option = input("Selecciona: ")

            if option == "1":
                self.view_stats()
            elif option == "2":
                self.update_profile()
            elif option == "3":
                print("Cerrando sesión...")
                time.sleep(2)
                break
            else:
                print("Opción inválida")
                time.sleep(2)

    def view_stats(self):
        """Muestra las estadísticas del jugador (por implementar)."""
        pass

    def update_profile(self):
        """Permite actualizar nombre y edad del jugador (por implementar)."""
        pass


# -------------------------------
# Menú de Staff
# -------------------------------
class StaffMenu:
    """
    Menú específico para miembros del club.
    Permite ver jugadores del equipo, buscar jugadores, crear equipo, etc.
    """

    def __init__(self, staff):
        self.staff = staff

    def show(self):
        """
        Muestra el menú del staff en un bucle.
        """
        while True:
            print("=== MENÚ STAFF ===")
            print("1. Ver jugadores del equipo propio")
            print("2. Actualizar perfil")
            print("3. Buscar jugadores externos")
            print("4. Crear equipo")
            print("5. Cerrar sesión")
            option = input("Selecciona: ")

            if option == "1":
                self.view_team_players()
            elif option == "2":
                self.update_profile()
            elif option == "3":
                self.search_players()
            elif option == "4":
                self.create_team()
            elif option == "5":
                print("Cerrando sesión...")
                time.sleep(2)
                break
            else:
                print("Opción inválida")
                time.sleep(2)

    def view_team_players(self):
        """Muestra la lista de jugadores del equipo del staff (por implementar)."""
        pass

    def update_profile(self):
        """Permite actualizar datos del staff (por implementar)."""
        pass

    def search_players(self):
        """Permite buscar jugadores externos (por implementar)."""
        pass

    def create_team(self):
        """Permite crear un nuevo equipo (por implementar)."""
        pass


# -------------------------------
# Menú de Árbitro
# -------------------------------
class RefereeMenu:
    """
    Menú específico para árbitros.
    Permite verificar partidos, actualizar perfil y exportar información de jugadores.
    """

    def __init__(self, referee):
        self.referee = referee

    def show(self):
        """
        Muestra el menú del árbitro en un bucle.
        """
        while True:
            print("=== MENÚ ÁRBITRO ===")
            print("1. Verificar partidos")
            print("2. Ver/Actualizar perfil")
            print("3. Exportar archivos de jugadores")
            print("4. Cerrar sesión")
            option = input("Selecciona: ")

            if option == "1":
                self.verify_matches()
            elif option == "2":
                self.update_profile()
            elif option == "3":
                self.export_players()
            elif option == "4":
                print("Cerrando sesión...")
                time.sleep(2)
                break
            else:
                print("Opción inválida")
                time.sleep(2)

    def verify_matches(self):
        """Permite verificar partidos asignados (por implementar)."""
        pass

    def update_profile(self):
        """Permite actualizar datos del árbitro (por implementar)."""
        pass

    def export_players(self):
        """Permite exportar datos de jugadores (por implementar)."""
        pass


# -------------------------------
# Ejecución del programa
# -------------------------------
if __name__ == "__main__":
    MainMenu().show()