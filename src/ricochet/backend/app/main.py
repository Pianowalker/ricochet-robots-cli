from fastapi import FastAPI
from ricochet.backend.app.api.routes.practice import router as practice_router

app = FastAPI()

app.include_router(practice_router)


@app.get("/")
def root():
    return {"message": "Ricochet Robots API running"}