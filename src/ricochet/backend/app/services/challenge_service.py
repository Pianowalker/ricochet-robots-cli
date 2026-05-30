from ricochet.backend.app.services.practice_service import PracticeService
from ricochet.domain.sessions.challenge_session import ChallengeSession


class ChallengeService(PracticeService):

    session_class = ChallengeSession