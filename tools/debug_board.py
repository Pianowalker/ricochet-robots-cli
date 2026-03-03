from ricochet.domain.game import Game
from ricochet.domain.maps import create_yellow_quadrant_v3

DISPLAY_MAP = {
    "blue": "B",
    "yellow": "Y",
    "green": "G",
    "red": "R"
}

COLORS = {
    "R": "\033[91m",   # rojo
    "G": "\033[92m",   # verde
    "Y": "\033[93m",   # amarillo
    "B": "\033[94m",   # azul
    "*": "\033[95m",   # comodín
    "RESET": "\033[0m"
}


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

        middle_line = f"{r:2} |"

        for c in range(game.width):

            cell = "."
            display_cell = cell

            # -------- TARGETS --------
            for target in game.targets:
                if target.position == (r, c):
                    if target.color is None:
                        cell = "*"
                    else:
                        cell = DISPLAY_MAP[target.color].lower()

            # -------- BUMPERS --------
            if (r, c) in game.bumpers:
                bumper = game.bumpers[(r, c)]
                cell = bumper.diagonal

                color_key = DISPLAY_MAP[bumper.color]
                color_code = COLORS[color_key]
                display_cell = f"{color_code}{cell}{COLORS['RESET']}"

            else:
                display_cell = cell

                # Colorear targets
                if cell == "*":
                    display_cell = f"{COLORS['*']}{cell}{COLORS['RESET']}"
                elif cell.upper() in COLORS:
                    display_cell = f"{COLORS[cell.upper()]}{cell}{COLORS['RESET']}"

            # Robots (sobrescriben todo)
            for robot in game.robots.values():
                if robot.position == (r, c):
                    robot_letter = DISPLAY_MAP[robot.color]
                    display_cell = f"{COLORS[robot_letter]}{robot_letter}{COLORS['RESET']}"

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


def main():
    q = create_yellow_quadrant_v3()

    print("\n=== CUADRANTE ORIGINAL ===")
    print_single_quadrant(q)

    print_rotations(q)


if __name__ == "__main__":
    main()