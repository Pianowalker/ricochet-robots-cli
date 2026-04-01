from ricochet.domain.maps import build_random_board
from ricochet.domain.sessions.single_player_session import SinglePlayerSession

class GameService:

    def create_session(self, rounds=5, mode="random", difficulty="normal"):
        colors = ["blue", "yellow", "green", "red"]

        if difficulty == "easy":
            colors.append("gray")

        game = build_random_board(mode=mode)
        game.place_robots_randomly(colors)

        session = SinglePlayerSession(game, total_rounds=rounds)

        return session