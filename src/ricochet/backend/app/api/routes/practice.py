from fastapi import APIRouter
from ricochet.backend.app.services.practice_service import PracticeService
from ricochet.backend.app.services.serializer import serialize_game
from ricochet.backend.app.store import store

router = APIRouter()

service = PracticeService()


@router.post("/practice")
def create_practice():
    session = service.create_session()
    session_id = store.create(session)

    return {
        "session_id": session_id,
        "state": serialize_game(session.game)
    }