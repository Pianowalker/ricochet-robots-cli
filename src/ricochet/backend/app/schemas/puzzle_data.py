from pydantic import BaseModel


class PuzzleData(BaseModel):
    name:       str
    board_size: int
    walls:      list
    bumpers:    list
    robots:     dict
    target:     dict
