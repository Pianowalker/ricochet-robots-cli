import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

from ricochet.domain.maps import (
    GREEN_QUADRANTS, BLUE_QUADRANTS, RED_QUADRANTS, YELLOW_QUADRANTS,
)
from ricochet.backend.app.schemas.puzzle_data import PuzzleData

router = APIRouter(prefix="/editor", tags=["editor"])

PUZZLES_DIR = Path(__file__).parents[2] / "data" / "puzzles" / "tutorial"

ALL_QUADRANTS = {
    "green":  GREEN_QUADRANTS,
    "blue":   BLUE_QUADRANTS,
    "red":    RED_QUADRANTS,
    "yellow": YELLOW_QUADRANTS,
}


def _serialize_quadrant(q):
    """Return walls and bumpers of a Quadrant in list format (8x8 coords)."""
    walls = []
    for wall in q.walls:
        cell1, cell2 = tuple(wall)
        walls.append([list(cell1), list(cell2)])

    bumpers = [
        {"position": list(b.position), "diagonal": b.diagonal, "color": b.color}
        for b in q.bumpers
    ]

    return {
        "board_size": q.size,
        "walls": walls,
        "bumpers": bumpers,
    }


# ── GET /editor/quadrants ─────────────────────────────────────────────────────

@router.get("/quadrants")
def list_quadrants():
    """Return the list of all available quadrants."""
    result = []
    for color, factories in ALL_QUADRANTS.items():
        for variant, factory in enumerate(factories, start=1):
            q = factory()
            result.append({
                "color":       color,
                "variant":     variant,
                "has_bumpers": q.has_bumpers,
            })
    return result


# ── GET /editor/quadrant/{color}/{variant} ────────────────────────────────────

@router.get("/quadrant/{color}/{variant}")
def get_quadrant(color: str, variant: int, rotation: int = 0):
    """
    Return walls and bumpers for a single quadrant (no robots, no targets).
    rotation: 0-3 (number of 90° clockwise rotations).
    """
    factories = ALL_QUADRANTS.get(color)
    if not factories:
        raise HTTPException(status_code=404, detail=f"Color '{color}' not found")
    if variant < 1 or variant > len(factories):
        raise HTTPException(status_code=404, detail=f"Variant {variant} not found")

    q = factories[variant - 1]()
    if rotation:
        q = q.rotate(rotation)

    return _serialize_quadrant(q)


# ── POST /editor/puzzle ───────────────────────────────────────────────────────

@router.post("/puzzle")
def save_puzzle(puzzle: PuzzleData):
    """Save a puzzle as JSON to puzzles/tutorial/{name}.json."""
    PUZZLES_DIR.mkdir(parents=True, exist_ok=True)

    path = PUZZLES_DIR / f"{puzzle.name}.json"
    data = puzzle.model_dump()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"saved": str(path), "name": puzzle.name}
