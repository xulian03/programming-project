import time

class User:
    def __init__(self, id, name, age, password):
        self.id = id
        self.name = name
        self.age = age
        self.password = password

    def check_password(self, password):
        return self.password == password


class Player(User):
    def __init__(self, id, name, age, password, position, team):
        super().__init__(id, name, age, password)
        self.position = position
        self.team = team


class ClubMember(User):
    def __init__(self, id, name, age, password, team, role):
        super().__init__(id, name, age, password)
        self.team = team
        self.role = role


class Referee(User):
    def __init__(self, id, name, age, password, license):
        super().__init__(id, name, age, password)
        self.license = license


class MainMenu:
    def __init__(self):
        self.users = []

    def show(self):
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
        print("=== REGISTRO ===")
        print("1. Jugador")
        print("2. Staff")
        print("3. Árbitro")
        user_type = input("Selecciona el tipo de usuario: ")

        id = input("ID: ")
        name = input("Nombre: ")
        age = int(input("Edad: "))
        password = input("Contraseña: ")

        if len(password) < 6:
            print("La contraseña debe tener mínimo 6 caracteres")
            time.sleep(2)
            return

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
        print("=== INICIO DE SESIÓN ===")
        id = input("ID: ")
        password = input("Contraseña: ")

        user = next((u for u in self.users if u.id == id and u.check_password(password)), None)

        if user:
            print("Inicio de sesión exitoso")
            time.sleep(2)
            if isinstance(user, Player):
                PlayerMenu(user).show()
            elif isinstance(user, ClubMember):
                StaffMenu(user).show()
            elif isinstance(user, Referee):
                RefereeMenu(user).show()
        else:
            print("Credenciales incorrectas")
            time.sleep(2)


class PlayerMenu:
    def __init__(self, player):
        self.player = player

    def show(self):
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
        pass

    def update_profile(self):
        pass


class StaffMenu:
    def __init__(self, staff):
        self.staff = staff

    def show(self):
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
        pass

    def update_profile(self):
        pass

    def search_players(self):
        pass

    def create_team(self):
        pass


class RefereeMenu:
    def __init__(self, referee):
        self.referee = referee

    def show(self):
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
        pass

    def update_profile(self):
        pass

    def export_players(self):
        pass


if __name__ == "__main__":
    MainMenu().show()