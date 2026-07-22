from pydantic import BaseModel

from app.enums import ActivityLevel, ExperienceLevel, Species, Trait


class Pet(BaseModel):
    id: int
    name: str
    species: Species
    breed: str
    age: int
    energy_level: ActivityLevel
    apartment_friendly: bool
    experience_required: ExperienceLevel
    personality_traits: list[Trait]
    good_with_children: bool
    good_with_dogs: bool
    good_with_cats: bool
    notes: str
