from app.enums import (
    ActivityLevel,
    AgePreference,
    ExperienceLevel,
    HouseholdMember,
    HousingType,
    SpeciesPreference,
    Trait,
)
from app.schemas import AdopterProfile, Pet, PetMatch

ACTIVITY_LEVELS = {
    ActivityLevel.LOW: 0,
    ActivityLevel.MODERATE: 1,
    ActivityLevel.HIGH: 2,
}

EXPERIENCE_LEVELS = {
    ExperienceLevel.BEGINNER: 0,
    ExperienceLevel.INTERMEDIATE: 1,
    ExperienceLevel.ADVANCED: 2,
}

AGE_LEVELS = {
    AgePreference.YOUNG: 0,
    AgePreference.ADULT: 1,
    AgePreference.SENIOR: 2,
}


def is_eligible(
    profile: AdopterProfile,
    pet: Pet,
) -> bool:
    if (
        profile.preferred_species != SpeciesPreference.NO_PREFERENCE
        and profile.preferred_species.value != pet.species.value
    ):
        return False

    if (
        profile.housing_type == HousingType.APARTMENT
        and not pet.apartment_friendly
    ):
        return False

    if (
        HouseholdMember.CHILDREN in profile.household
        and not pet.good_with_children
    ):
        return False

    if (
        HouseholdMember.DOGS in profile.household
        and not pet.good_with_dogs
    ):
        return False

    if (
        HouseholdMember.CATS in profile.household
        and not pet.good_with_cats
    ):
        return False

    return True


def get_age_bucket(age: int) -> AgePreference:
    # Young: 0-2, Adult: 3-7, Senior: 8+
    if age <= 2:
        return AgePreference.YOUNG

    if age <= 7:
        return AgePreference.ADULT

    return AgePreference.SENIOR


def calculate_age_score(
    profile: AdopterProfile,
    pet: Pet,
) -> float:
    if profile.preferred_age == AgePreference.NO_PREFERENCE:
        return 25.0

    adopter_level = AGE_LEVELS[profile.preferred_age]
    pet_level = AGE_LEVELS[get_age_bucket(pet.age)]

    difference = abs(adopter_level - pet_level)

    if difference == 0:
        return 25.0

    if difference == 1:
        return 12.5

    return 0.0


def calculate_activity_score(
    profile: AdopterProfile,
    pet: Pet,
) -> float:
    adopter_level = ACTIVITY_LEVELS[profile.activity_level]
    pet_level = ACTIVITY_LEVELS[pet.energy_level]

    difference = abs(adopter_level - pet_level)

    if difference == 0:
        return 25.0

    if difference == 1:
        return 12.5

    return 0.0


def calculate_experience_score(
    profile: AdopterProfile,
    pet: Pet,
) -> float:
    adopter_level = EXPERIENCE_LEVELS[profile.experience_level]
    required_level = EXPERIENCE_LEVELS[pet.experience_required]

    difference = adopter_level - required_level

    if difference >= 0:
        return 25.0

    if difference == -1:
        return 12.5

    return 0.0


def get_matched_traits(
    profile: AdopterProfile,
    pet: Pet,
) -> list[Trait]:
    preferred = set(profile.preferred_traits)
    pet_traits = set(pet.personality_traits)

    return sorted(
        preferred.intersection(pet_traits),
        key=lambda trait: trait.value,
    )


def calculate_trait_score(
    profile: AdopterProfile,
    pet: Pet,
) -> float:
    if not profile.preferred_traits:
        return 25.0

    matched_traits = get_matched_traits(profile, pet)

    match_ratio = (
        len(matched_traits)
        / len(set(profile.preferred_traits))
    )

    return round(match_ratio * 25, 1)


def calculate_score(
    profile: AdopterProfile,
    pet: Pet,
) -> float:
    total = (
        calculate_age_score(profile, pet)
        + calculate_activity_score(profile, pet)
        + calculate_experience_score(profile, pet)
        + calculate_trait_score(profile, pet)
    )

    return round(min(max(total, 0.0), 100.0), 1)


def get_matches(
    profile: AdopterProfile,
    pets: list[Pet],
) -> list[PetMatch]:
    matches = [
        PetMatch(
            pet=pet,
            score=calculate_score(profile, pet),
            matched_traits=get_matched_traits(profile, pet),
        )
        for pet in pets
        if is_eligible(profile, pet)
    ]

    return sorted(matches, key=lambda match: match.score, reverse=True)
