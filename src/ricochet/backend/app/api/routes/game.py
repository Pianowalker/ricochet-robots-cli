from fastapi import APIRouter
from ricochet.backend.app.schemas.game_request import GameRequest
from ricochet.backend.app.services.game_service import GameService
from ricochet.backend.app.store import store
from ricochet.backend.app.services.serializer import serialize_session

router = APIRouter()
service = GameService()

@router.post("/game")
def create_game(request: GameRequest):
    session = service.create_session(
        rounds=request.rounds,
        mode=request.mode,
        difficulty=request.difficulty
    )

    session_id = store.create(session)

    return {
        "session_id": session_id,
        "state": serialize_session(session)
    }