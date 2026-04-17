from fastapi import FastAPI
from ricochet.backend.app.api.routes.practice import router as practice_router
from ricochet.backend.app.api.routes.game import router as game_router
from ricochet.backend.app.api.routes.editor import router as editor_router
from ricochet.backend.app.api.routes.tutorial import router as tutorial_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(practice_router)
app.include_router(game_router)
app.include_router(editor_router)
app.include_router(tutorial_router)


@app.get("/")
def root():
    return {"message": "Ricochet Robots API running"}