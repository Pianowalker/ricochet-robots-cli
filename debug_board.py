from game import Game
from maps import create_red_quadrant_v4


def print_single_quadrant(quadrant):
    game = Game(8, 8)
    game.load_quadrant(quadrant)
    print_board_debug(game)


def print_rotations(quadrant):
    for i in range(4):
        print(f"\n=== Rotación {i * 90}° ===")
        rotated = quadrant.rotate(i)
        print_single_quadrant(rotated)

def print_board_debug(game):
    print()

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

            # Mostrar TODOS los targets
            for target in game.targets:
                if target.position == (r, c):
                    if target.color is None:
                        cell = "*"     # comodín
                    else:
                        cell = target.color.lower()

            # Bumper
            if (r, c) in game.bumpers:
                bumper = game.bumpers[(r, c)]
                cell = bumper.diagonal

            # Robot (sobrescribe todo)
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
    q = create_red_quadrant_v4()

    print("\n=== CUADRANTE ORIGINAL ===")
    print_single_quadrant(q)

    print_rotations(q)


if __name__ == "__main__":
    main()