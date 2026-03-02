from ricochet.domain.game import Game
from ricochet.domain.models import Bumper
from ricochet.domain.sessions import SinglePlayerSession

def test_session_does_not_count_illegal_move():
    game = Game(4, 4)

    # Bumper azul
    game.bumpers[(1, 1)] = Bumper((1, 1), "/", "blue")

    # Pared arriba (bloquea rebote)
    game.add_wall((1, 1), (0, 1))

    # Robot amarillo
    game.add_robot("Y", (1, 0))

    session = SinglePlayerSession(game, total_rounds=1)
    session.current_round = 1
    session.round_active = True
    session.declared_moves = 3
    session.move_count = 0

    position, won, message = session.move("Y", "right")

    assert session.move_count == 0
    assert session.round_active is True