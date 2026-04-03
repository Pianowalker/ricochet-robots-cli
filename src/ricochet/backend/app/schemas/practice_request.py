from pydantic import BaseModel

class PracticeRequest(BaseModel):
    mode: str = "random"
    difficulty: str = "normal"