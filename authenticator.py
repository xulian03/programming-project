import utils

def auth():
    print(utils.separator())
    print(utils.title_style("TIPO DE USUARIO"))
    print()
    print(utils.default_text("A continuación, por favor seleccione su tipo de usuario"))
    print(utils.separator())
    utils.options("Jugador", "Entrenador", "Arbitro", "Salir")

# Hola 