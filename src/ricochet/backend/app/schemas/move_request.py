from pydantic import BaseModel


class MoveRequest(BaseModel):
    color: str
    direction: str