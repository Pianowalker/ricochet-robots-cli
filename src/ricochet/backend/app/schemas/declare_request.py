from pydantic import BaseModel


class DeclareRequest(BaseModel):
    moves: int