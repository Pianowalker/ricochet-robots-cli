from fastapi import APIRouter, HTTPException
from ricochet.backend.app.schemas.declare_request import DeclareRequest
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


@router.post("/game/{session_id}/round/start")
def start_round(session_id: str):
    session = store.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    success = session.start_new_round()

    if not success:
        raise HTTPException(status_code=400, detail="No more rounds available")

    return {
    "event": {
        "type": "round_started",
        "round": session.current_round
    },
    "state": serialize_session(session)
}


@router.post("/game/{session_id}/declare")
def declare_moves(session_id: str, request: DeclareRequest):
    session = store.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.round_active:
        raise HTTPException(status_code=400, detail="No active round")

    if session.declared_moves is not None:
        raise HTTPException(status_code=400, detail="Already declared")

    session.declare_solution(request.moves)

    return {
        "event": {
            "type": "declared",
            "moves": request.moves
        },
        "state": serialize_session(session)
    }