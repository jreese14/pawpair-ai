from pydantic import BaseModel

from app.enums import (
    ActivityLevel,
    AgePreference,
    AvailableTime,
    ExperienceLevel,
    Gender,
    HouseholdMember,
    HousingType,
    Species,
    SpeciesPreference,
    Trait,
)


class Pet(BaseModel):
    id: int
    name: str
    pet_image: str = "https://picsum.photos/300/300"
    species: Species
    gender: Gender
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


class AdopterProfile(BaseModel):
    name: str
    preferred_species: SpeciesPreference
    preferred_age: AgePreference
    housing_type: HousingType
    activity_level: ActivityLevel
    available_time: AvailableTime
    experience_level: ExperienceLevel
    preferred_traits: list[Trait]
    household: list[HouseholdMember]


class PetMatch(BaseModel):
    pet: Pet
    score: float
    matched_traits: list[Trait]


class ExplanationRequest(BaseModel):
    adopter_profile: AdopterProfile
    pet: Pet
    matched_traits: list[Trait]
    score: float
