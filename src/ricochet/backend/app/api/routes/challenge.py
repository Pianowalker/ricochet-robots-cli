from fastapi import APIRouter, HTTPException
from ricochet.backend.app.store import store
from ricochet.backend.app.schemas.move_request import MoveRequest
from ricochet.backend.app.schemas.practice_request import PracticeRequest
from ricochet.backend.app.services.challenge_service import ChallengeService
from ricochet.backend.app.services.serializer import serialize_session


router = APIRouter()

service = ChallengeService()


@router.post("/challenge")
def create_challenge(request: PracticeRequest = PracticeRequest()):
    session = service.create_session(
        mode=request.mode,
        difficulty=request.difficulty
    )
    session.start()
    session_id = store.create(session)

    return {
        "session_id": session_id,
        "state": serialize_session(session)
    }


# Arranca el cronómetro del desafío. Hasta que se llame, el timer está en 300s y los movimientos están bloqueados.
@router.post("/challenge/{session_id}/start")
def start_challenge(session_id: str):
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.start()

    return {
        "state": serialize_session(session)
    }


# Mueve un robot en la sesión de challenge especificada por session_id, utilizando los datos de MoveRequest.
@router.post("/challenge/{session_id}/move")
def move_robot(session_id: str, request: MoveRequest):
    # Recupera la sesión de challenge del store utilizando session_id. Si no se encuentra, devuelve error.
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    position, won, message, waypoints, earned_points = session.move(
        request.color,
        request.direction
    )
    # Devuelve el nuevo estado del juego, si se ha ganado, un mensaje, los waypoints del movimiento y los puntos ganados.
    return {
        "event": {
            "won": won,
            "message": message,
            "waypoints": waypoints,
            "earned_points": earned_points
        },
        "state": serialize_session(session)
    }


@router.post("/challenge/{session_id}/skip")
def skip_puzzle(session_id: str):

    session = store.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    penalty = session.skip_puzzle()

    return {
        "event": {
            "message": "Puzzle salteado",
            "penalty": penalty
        },
        "state": serialize_session(session)
    }
