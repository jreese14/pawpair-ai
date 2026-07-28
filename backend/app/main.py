from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import match_engine
from app.pet_repository import PetRepository
from app.schemas import AdopterProfile, Pet, PetMatch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pet_repository = PetRepository()


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "PawPair API is running"}


@app.get("/pets")
def get_pets() -> list[Pet]:
    return pet_repository.get_all()


@app.post("/matches")
def get_matches(profile: AdopterProfile) -> list[PetMatch]:
    return match_engine.get_matches(profile, pet_repository.get_all())


