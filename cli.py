from game import Game


def print_board(game):
    print()

    # ---- Números de columnas ----
    header = "    "
    for c in range(game.width):
        header += f" {c}  "
    print(header)

    for r in range(game.height):

        # ---- Línea superior de la fila ----
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

        # ---- Línea con contenido ----
        middle_line = f"{r:2} |"

        for c in range(game.width):

            # contenido celda
            cell = "."
            for robot in game.robots.values():
                if robot.position == (r, c):
                    cell = robot.color

            middle_line += f" {cell} "

            # pared vertical
            if c < game.width - 1:
                if frozenset({(r, c), (r, c+1)}) in game.walls:
                    middle_line += "|"
                else:
                    middle_line += " "
            else:
                middle_line += "|"

        print(middle_line)

    # ---- Línea inferior final ----
    bottom_line = "   +"
    for _ in range(game.width):
        bottom_line += "---+"
    print(bottom_line)

    print()


def main():
    game = Game(6, 6)

    # Robots iniciales
    game.add_robot("R", (2, 2))
    game.add_robot("B", (3, 4))
    game.add_robot("G", (4, 1))

    # Pared de prueba
    game.add_wall((2, 2), (2, 3))  # bloquea derecha inmediata
    game.add_wall((4, 2), (5, 2))  # bloquea una casilla antes de tocar el suelo si baja
    game.add_wall((4, 4), (4, 5))
    print("Controles: right, left, up, down")
    print("Escribí 'q' para salir")

    while True:
        print_board(game)
        command = input("Comando (ej: R r) o 'q': ")

        if command == "q":
            break

        try:
            robot_letter, direction_letter = command.split()

            direction_map = {
                "r": "right",
                "l": "left",
                "u": "up",
                "d": "down"
            }

            direction = direction_map[direction_letter]

            new_pos = game.move(robot_letter, direction)
            print(f"{robot_letter} -> {new_pos}")

        except ValueError:
            print("Formato inválido. Usar: <ROBOT> <r/l/u/d>")
        except KeyError:
            print("Robot o dirección inválida.")


if __name__ == "__main__":
    main()