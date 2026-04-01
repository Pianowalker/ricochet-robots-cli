from pydantic import BaseModel


class GameRequest(BaseModel):
    rounds: int = 5
    mode: str = "random"
    difficulty: str = "normal"