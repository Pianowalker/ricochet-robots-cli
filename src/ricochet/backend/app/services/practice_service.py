from ricochet.domain.maps import build_random_board
from ricochet.domain.sessions.practice_session import PracticeSession


class PracticeService:

    session_class = PracticeSession

    def create_session(self, mode="random", difficulty="normal"):
        colors = ["blue", "yellow", "green", "red"]

        if difficulty == "easy":
            colors.append("gray")

        game = build_random_board(mode=mode)
        game.place_robots_randomly(colors)

        session = self.session_class(game)
        session.start_puzzle()

        return session