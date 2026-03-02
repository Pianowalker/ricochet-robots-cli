import sys
from pathlib import Path

# Allow running this test file directly from the repo root or from the editor
# by ensuring the project root is on sys.path (convenience for local debugging).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain.game import Game
from domain.models import Bumper
from domain.sessions import SinglePlayerSession

def main():
    # --- Setup mínimo ---
    game = Game(4, 4)

    # Bumper amarillo
    game.bumpers[(1, 1)] = Bumper((1, 1), "/", "yellow")

    # Pared a la derecha del bumper
    game.add_wall((1, 1), (1, 2))

    # Robot amarillo a la izquierda
    game.add_robot("Y", (1, 0))

    # Creamos sesión
    session = SinglePlayerSession(game, total_rounds=1)

    # Forzamos estado de ronda manualmente
    session.current_round = 1
    session.round_active = True
    session.declared_moves = 3
    session.move_count = 0

    print("Posición inicial:", game.robots["Y"].position)

    # --- Movimiento ilegal ---
    position, won, message = session.move("Y", "right")

    print("\nResultado del movimiento:")
    print("Mensaje:", message)
    print("move_count:", session.move_count)
    print("round_active:", session.round_active)
    print("Posición real del robot:", game.robots["Y"].position)

if __name__ == "__main__":
    main()