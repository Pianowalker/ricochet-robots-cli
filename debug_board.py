from game import Game
from maps import create_yellow_quadrant_v1
from cli import print_board


def print_single_quadrant(quadrant):
    game = Game(8, 8)
    game.load_quadrant(quadrant)
    print_board(game)


def print_rotations(quadrant):
    for i in range(4):
        print(f"\n=== Rotación {i * 90}° ===")
        rotated = quadrant.rotate(i)
        print_single_quadrant(rotated)


def main():
    q = create_yellow_quadrant_v1()

    print("\n=== CUADRANTE ORIGINAL ===")
    print_single_quadrant(q)

    print_rotations(q)


if __name__ == "__main__":
    main()