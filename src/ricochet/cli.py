from email import message

from ricochet.domain.maps import build_random_board
from ricochet.domain.sessions import SinglePlayerSession
import os

# Habilitar ANSI en Windows
if os.name == "nt":
    os.system("")

COLORS = {
    "R": "\033[91m",   # rojo
    "G": "\033[92m",   # verde
    "Y": "\033[93m",   # amarillo
    "B": "\033[94m",   # azul
    "*": "\033[95m",   # comodín (magenta)
    "RESET": "\033[0m"
}

DISPLAY_MAP = {
    "blue": "B",
    "yellow": "Y",
    "green": "G",
    "red": "R"
}


def print_board(game):
    print()

    # Encabezado columnas
    header = "    "
    for c in range(game.width):
        header += f" {c}  "
    print(header)

    for r in range(game.height):

        # Línea superior
        top_line = "   +"
        for c in range(game.width):
            if r == 0:
                top_line += "---+"
            else:
                if frozenset({(r-1, c), (r, c)}) in game.walls:
                    top_line += "---+"
                else:
                    top_line += "   +"
        print(top_line)
        
        # Línea contenido
        middle_line = f"{r:2} |"

        for c in range(game.width):

            cell = "."

            # Primero target
            for target in game.targets:
                if target.position == (r, c):
                    if target == game.active_target:
                        if target.color is None:
                            cell = "*"
                        else:
                            cell = DISPLAY_MAP[target.color].lower()
                    else:
                        cell = "·"

                        # Bumper
            if (r, c) in game.bumpers:
                bumper = game.bumpers[(r, c)]
                cell = bumper.diagonal  # "/" o "\"
                bumper_color = bumper.color

            # Después robot (sobrescribe)
            for robot in game.robots.values():
                if robot.position == (r, c):
                    cell = DISPLAY_MAP[robot.color]

            # Aplicar color si corresponde
            display_cell = cell

            # Si es bumper, usar su color
            if (r, c) in game.bumpers:
                bumper = game.bumpers[(r, c)]
                color_name = bumper.color.lower()

                color_map = {
                    "red": "R",
                    "green": "G",
                    "yellow": "Y",
                    "blue": "B"
                }

                if color_name in color_map:
                    color_key = color_map[color_name]
                    color_code = COLORS[color_key]
                    display_cell = f"{color_code}{display_cell}{COLORS['RESET']}"

            # Si no es bumper, usar lógica normal
            elif isinstance(display_cell, str) and display_cell.upper() in COLORS:
                color_code = COLORS[display_cell.upper()]
                display_cell = f"{color_code}{display_cell}{COLORS['RESET']}"

            middle_line += f" {display_cell} "

            if c < game.width - 1:
                if frozenset({(r, c), (r, c+1)}) in game.walls:
                    middle_line += "|"
                else:
                    middle_line += " "
            else:
                middle_line += "|"

        print(middle_line)

    bottom_line = "   +"
    for _ in range(game.width):
        bottom_line += "---+"
    print(bottom_line)

    print()


def show_rules():
    print("\n=== REGLAS ===")
    print("""
- Los robots están representados por letras mayúsculas: B, R, Y, G.
- Los objetivos están representados por letras minúsculas: b, r, y, g.
- Debes calcular cuantos movimientos necesitas para que el robot cuya letra sea la misma que la del objetivo llegue a la casilla de este último.
- Una vez declarado esto, ganas un punto si consigues hacer esto en la cantidad de movimientos declarada.
- Existe también el objetivo comodín (*) que se puede alcanzar con un robot de cualquier color.
- Los robots se deslizan hasta chocar con pared, robot o borde.
- Los resortes (/\) reflejan el movimiento.
- Están prohibidos los movimientos ilegales, como terminar sobre un resorte o intentar mover un robot que no existe.
- Si el robot es del mismo color que el resorte, no rebota.
- +1 punto si acertás la cantidad exacta.
- -1 punto si no.
    """)


def show_controls():
    print("\n=== CONTROLES ===")
    print("""
Formato de movimiento: RL, BU, YD, etc.

Primera letra:
R = Rojo
B = Azul
G = Verde
Y = Amarillo

Segunda letra:
L = izquierda
R = derecha
U = arriba
D = abajo

Ejemplo:
Rl  → mueve el robot rojo hacia la izquierda
Bd  → mueve el robot azul hacia abajo
    """)

def main():
    while True:
        print("\n=== RICOCHET ROBOTS ===")
        print("1) Jugar")
        print("2) Ver reglas")
        print("3) Ver controles")
        print("4) Salir")

        option = input("Elegí una opción: ").strip()

        if option == "1":
            break
        elif option == "2":
            show_rules()
        elif option == "3":
            show_controls()
        elif option == "4":
            return
        else:
            print("Opción inválida.")

    while True:

        print("\nModo de mapa:")
        print("1) Aleatorio")
        print("2) Sin bumpers (fácil)")
        print("3) Al menos un bumper")

        option = input("Elegí modo: ").strip()

        mode_map = {
            "1": "random",
            "2": "no_bumpers",
            "3": "at_least_one_bumper"
        }

        if option in mode_map:
            mode = mode_map[option]
            break
        else:
            print("Opción inválida.")
    game = build_random_board(mode=mode)
    game.place_robots_randomly(["blue", "yellow", "green", "red"])

    max_rounds = len(game.targets)

    while True:
        try:
            chosen = int(input(f"¿Cuántas rondas? (1–{max_rounds}): "))

            if 1 <= chosen <= max_rounds:
                break
            else:
                print("Número fuera de rango.")

        except ValueError:
            print("Ingresá un número válido.")
    session = SinglePlayerSession(game, total_rounds=chosen)

    while True:

        started = session.start_new_round()

        target = session.game.active_target

        if target.color is None:
            print("Objetivo: COMODÍN (*)")
        else:
            print(f"Objetivo: {target.color.lower()}")

        if not started:
            print("\nPartida terminada.")
            print("Score final:", session.score)

            if session.score > 0:
                print("Resultado: Victoria 🎉")
            elif session.score < 0:
                print("Resultado: Derrota 😞")
            else:
                print("Resultado: Empate 🤝")

            break

        print(f"\n=== Ronda {session.current_round}/{session.total_rounds} ===")
        print("Score actual:", session.score)

        print_board(game)

        # Declaración
        while True:
            try:
                declared = int(input("¿Cuántas movidas? "))
                if declared <= 0:
                    print("Debe ser un número positivo.")
                    continue
                session.declare_solution(declared)
                break
            except ValueError:
                print("Ingresá un número entero válido.")

        # Movimientos
        while session.round_active:

            print_board(game)

            current_move = session.move_count + 1
            total_moves = session.declared_moves

            if session.move_count == 0:
                prompt = f"Movimiento {current_move}/{total_moves} (ej: Rl): "
            else:
                prompt = f"Movimiento {current_move}/{total_moves}: "

            command = input(prompt).strip()

            try:
                command = command.strip()

                if len(command) != 2:
                    print("Formato inválido. Usá por ejemplo: Rl o Bd")
                    continue

                robot_letter = command[0].upper()
                direction_letter = command[1].lower()

                LETTER_TO_COLOR = {
                    "B": "blue",
                    "Y": "yellow",
                    "G": "green",
                    "R": "red"
                }

                robot_color = LETTER_TO_COLOR[robot_letter]

                if robot_letter not in ["R", "B", "G", "Y"]:
                    print("Robot inválido.")
                    continue

                if direction_letter not in ["l", "r", "u", "d"]:
                    print("Dirección inválida.")
                    continue

                direction_map = {
                    "r": "right",
                    "l": "left",
                    "u": "up",
                    "d": "down"
                }

                direction = direction_map[direction_letter]

                position, won, message, _ = session.move(robot_color, direction)

                print(message)
                print_board(game)

            except Exception as e:
                print("Error:", e)

        print("Fin de ronda.")
        print("Score actual:", session.score)


if __name__ == "__main__":
    main()