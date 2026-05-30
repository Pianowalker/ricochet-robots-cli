from fastapi import FastAPI
from ricochet.backend.app.api.routes.practice import router as practice_router
from ricochet.backend.app.api.routes.game import router as game_router
from ricochet.backend.app.api.routes.editor import router as editor_router
from ricochet.backend.app.api.routes.tutorial import router as tutorial_router
from ricochet.backend.app.api.routes.challenge import router as challenge_router
from ricochet.backend.app.api.routes.scores import router as scores_router
from ricochet.backend.app.db import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


app.include_router(practice_router)
app.include_router(game_router)
app.include_router(editor_router)
app.include_router(tutorial_router)
app.include_router(challenge_router)
app.include_router(scores_router)


@app.get("/")
def root():
    return {"message": "Ricochet Robots API running"}