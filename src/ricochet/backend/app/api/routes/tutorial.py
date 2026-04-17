from fastapi import APIRouter, HTTPException

from ricochet.backend.app.schemas.move_request import MoveRequest
from ricochet.backend.app.services.serializer import serialize_game
from ricochet.backend.app.store import store
from ricochet.domain.sessions.tutorial_session import TutorialSession
from ricochet.domain.sessions.tutorial_content import TUTORIAL_LEVELS

router = APIRouter()


def _tutorial_state(session: TutorialSession) -> dict:
    return {
        "game": serialize_game(session.game),
        "tutorial": {
            "level_num": session.level_number,
            "total_levels": session.total_levels,
            "instruction": session.current_instruction,
        },
    }


@router.post("/tutorial")
def create_tutorial():
    session = TutorialSession(TUTORIAL_LEVELS)
    session_id = store.create(session)
    return {
        "session_id": session_id,
        "state": _tutorial_state(session),
    }


@router.post("/tutorial/{session_id}/move")
def move_robot(session_id: str, request: MoveRequest):
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = session.move(request.color, request.direction)
    return {
        "event": {
            "accepted": result.accepted,
            "message": result.message,
            "waypoints": result.waypoints,
            "level_complete": result.level_complete,
            "tutorial_complete": result.tutorial_complete,
        },
        "state": _tutorial_state(session),
    }


@router.post("/tutorial/{session_id}/next")
def next_level(session_id: str):
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.advance_level()
    return {
        "state": _tutorial_state(session),
    }
