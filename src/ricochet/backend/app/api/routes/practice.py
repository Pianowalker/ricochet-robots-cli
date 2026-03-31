from fastapi import APIRouter
from ricochet.backend.app.services.practice_service import PracticeService
from ricochet.backend.app.services.serializer import serialize_game
from ricochet.backend.app.store import store
from ricochet.backend.app.schemas.move_request import MoveRequest
from fastapi import HTTPException

router = APIRouter()

service = PracticeService()

""""
Crea una nueva sesión de práctica y devuelve el estado inicial del juego
instanciando PracticeSession y guardándola en el store con un ID único.
"""
@router.post("/practice")
def create_practice():
    session = service.create_session()
    session_id = store.create(session)

    return {
        "session_id": session_id,
        "state": serialize_game(session.game)
    }

# Mueve un robot en la sesión de práctica especificada por session_id, utilizando los datos de MoveRequest.
@router.post("/practice/{session_id}/move")
def move_robot(session_id: str, request: MoveRequest):
    # Recupera la sesión de práctica del store utilizando session_id. Si no se encuentra, devuelve error.
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    position, won, message, waypoints = session.move(
    request.color,
    request.direction   
)
    # Devuelve el nuevo estado del juego, si se ha ganado, un mensaje y los waypoints del movimiento.
    return {
    "state": serialize_game(session.game),
    "won": won,
    "message": message,
    "waypoints": waypoints
}