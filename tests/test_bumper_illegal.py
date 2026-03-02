import sys
from pathlib import Path

# Allow running this test file directly from the repo root or from the editor
# by ensuring the project root is on sys.path (convenience for local debugging).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain.game import Game
from domain.models import Bumper

def main():
    game = Game(4, 4)

    # Colocamos un bumper en (1,1)
    game.bumpers[(1,1)] = Bumper((1,1), "/", "yellow")

    # Colocamos una pared que bloquee el rebote
    # Supongamos que el robot viene desde la izquierda
    game.add_wall((1,1), (1,2))  # pared a la derecha del bumper

    # Robot amarillo en (1,0)
    game.add_robot("Y", (1,0))

    print("Posición inicial:", game.robots["Y"].position)

    position, won, illegal = game.move("Y", "right")

    print("Resultado:")
    print("Posición:", position)
    print("Ilegal:", illegal)
    print("Posición real del robot:", game.robots["Y"].position)

if __name__ == "__main__":
    main()