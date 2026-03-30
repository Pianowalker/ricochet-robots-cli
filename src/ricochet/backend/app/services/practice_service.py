from ricochet.domain.maps import build_random_board
from ricochet.domain.sessions.practice_session import PracticeSession

class PracticeService:

    def create_session(self, colors=None):
        if colors is None:
            colors = ["blue", "yellow", "green", "red"]

        game = build_random_board(mode="random")
        game.place_robots_randomly(colors)

        session = PracticeSession(game)
        session.start_puzzle()

        return session