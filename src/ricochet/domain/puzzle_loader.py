import json
from pathlib import Path

from .game import Game
from .models import Bumper, Target


def game_from_puzzle(data: dict) -> Game:
    """Build a ready-to-play Game from a puzzle dict.

    Compatible with ``PuzzleData.model_dump()`` and raw JSON-parsed dicts.
    The caller is responsible for loading and parsing the JSON.
    """
    size = data["board_size"]
    game = Game(size, size)

    for wall in data["walls"]:
        (r1, c1), (r2, c2) = wall
        game.add_wall((r1, c1), (r2, c2))

    for b in data["bumpers"]:
        pos = tuple(b["position"])
        game.bumpers[pos] = Bumper(pos, b["diagonal"], b["color"])

    for color, pos in data["robots"].items():
        game.add_robot(color, tuple(pos))

    t = data["target"]
    position = tuple(t["position"])
    game.targets.append(Target(t["color"], t.get("symbol"), position))
    game.active_target = game.targets[0]

    return game


def game_from_puzzle_file(path: str | Path) -> Game:
    """Load a puzzle JSON file and return a ready-to-play Game."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return game_from_puzzle(data)
