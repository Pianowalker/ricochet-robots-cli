from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ricochet.backend.app.db import NAME_MAX_LEN, Score, get_db


router = APIRouter()


class ScoreCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=NAME_MAX_LEN)
    score: int


class ScoreOut(BaseModel):
    id: int
    name: str
    score: int
    played_at: str


def _serialize(s: Score) -> dict:
    return {
        "id": s.id,
        "name": s.name,
        "score": s.score,
        "played_at": s.played_at.isoformat() + "Z",
    }


@router.post("/scores")
def create_score(payload: ScoreCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="El nombre no puede estar vacío")
    entry = Score(name=name[:NAME_MAX_LEN], score=payload.score)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return _serialize(entry)


@router.get("/scores")
def list_scores(limit: int = 100, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 500))
    rows = (
        db.query(Score)
        .order_by(desc(Score.score), desc(Score.played_at))
        .limit(limit)
        .all()
    )
    return [_serialize(r) for r in rows]
