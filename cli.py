from game import Game
from sessions import SinglePlayerSession
from maps import create_green_quadrant


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
                            cell = target.color.lower()
                    else:
                        cell = "·"

            # Después robot (sobrescribe)
            for robot in game.robots.values():
                if robot.position == (r, c):
                    cell = robot.color

            middle_line += f" {cell} "

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


def main():

    q = create_green_quadrant()
    q_rot = q.rotate_90()

    game = Game(8,8)
    game.load_quadrant(q_rot)
    
    game.place_robots_randomly(["R","B","G","Y"])

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

        if not started:
            print("\nPartida terminada.")
            print("Score final:", session.score)
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

            command = input("Movimiento (ej: R r): ")

            try:
                robot_letter, direction_letter = command.split()

                direction_map = {
                    "r": "right",
                    "l": "left",
                    "u": "up",
                    "d": "down"
                }

                direction = direction_map[direction_letter]

                position, won, message = session.move(robot_letter, direction)

                print(message)

            except Exception:
                print("Comando inválido.")

        print("Fin de ronda.")
        print("Score actual:", session.score)


if __name__ == "__main__":
    main()