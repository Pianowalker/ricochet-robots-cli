from ricochet.domain.game import Game
from ricochet.domain.models import Bumper

def test_bumper_illegal_move():
    game = Game(4, 4)

    # Bumper azul en (1,1)
    game.bumpers[(1, 1)] = Bumper((1, 1), "/", "blue")

    # Pared arriba del bumper
    game.add_wall((1, 1), (0, 1))

    # Robot amarillo a la izquierda
    game.add_robot("Y", (1, 0))

    _, _, illegal, _ = game.move("Y", "right")

    assert illegal is True
    assert game.robots["Y"].position == (1, 0)
    