import json
from pathlib import Path

from app.schemas import Pet

PETS_DATA_PATH = Path(__file__).parent / "data" / "pets.json"


class PetRepository:
    def __init__(self, data_path: Path = PETS_DATA_PATH):
        with open(data_path) as f:
            raw_pets = json.load(f)
        self._pets = [Pet(**pet) for pet in raw_pets]

    def get_all(self) -> list[Pet]:
        return list(self._pets)

    def get_by_id(self, pet_id: int) -> Pet:
        for pet in self._pets:
            if pet.id == pet_id:
                return pet
        raise ValueError(f"No pet found with id {pet_id}")
