from datetime import datetime
from ricochet.domain.sessions.practice_session import PracticeSession

class ChallengeSession(PracticeSession):

    def __init__(self, game):
        super().__init__(game)

        self.score = 0
        self.started_at = None
        self.duration_seconds = 300

    def start(self):
        if self.started_at is None:
            self.started_at = datetime.now()

    def is_started(self):
        return self.started_at is not None

    def get_remaining_time(self):
        if not self.is_started():
            return self.duration_seconds

        elapsed = datetime.now() - self.started_at
        remaining = self.duration_seconds - elapsed.total_seconds()

        return max(0, int(remaining))

    def is_finished(self):
        return self.is_started() and self.get_remaining_time() <= 0

    def calculate_points(self):
        points = max(25, 100 - self.move_count * 5)

        if self.move_count <= 7:
            points += 50

        return points

    def award_points(self):
        points = self.calculate_points()
        self.score += points
        return points

    def move(self, color, direction):
        if not self.is_started():
            return None, False, "Desafío no iniciado", [], 0

        if self.is_finished():
            return None, False, "Tiempo terminado", [], 0

        position, won, message, waypoints = super().move(color, direction)

        earned_points = 0

        if won:
            earned_points = self.award_points()
            self.start_puzzle()

        return position, won, message, waypoints, earned_points

    def skip_puzzle(self):
        if not self.is_started() or self.is_finished():
            return 0

        self.score -= 40
        self.start_puzzle()
        return 40
