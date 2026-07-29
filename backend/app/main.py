from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import match_engine
from app.pet_repository import PetRepository
from app.rag_service import RAGService
from app.schemas import AdopterProfile, Pet, PetMatch
from app.enums import Trait

from app.rag_service import RAGService

app = FastAPI()
rag_service = RAGService()

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


@app.post("/explanation")
def get_explanation(adopter_profile: AdopterProfile, pet: Pet, matched_traits: list[Trait], score: float) -> dict:
    rag_service = RAGService()
    explanation = rag_service.generate_match_explanation(adopter_profile, pet, matched_traits, score)
    return {"explanation": explanation}

@
