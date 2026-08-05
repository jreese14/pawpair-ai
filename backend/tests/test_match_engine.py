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
from app.match_engine import (
    calculate_activity_score,
    calculate_age_score,
    calculate_experience_score,
    calculate_score,
    calculate_trait_score,
    get_age_bucket,
    get_matched_traits,
    get_matches,
    is_eligible,
)
from app.schemas import AdopterProfile, Pet, PetMatch


def make_profile(**overrides):
    defaults = dict(
        name="Test Adopter",
        preferred_species=SpeciesPreference.NO_PREFERENCE,
        preferred_age=AgePreference.NO_PREFERENCE,
        housing_type=HousingType.HOUSE,
        activity_level=ActivityLevel.MODERATE,
        available_time=AvailableTime.TWO_TO_FOUR_HOURS,
        experience_level=ExperienceLevel.INTERMEDIATE,
        preferred_traits=[],
        household=[],
    )
    defaults.update(overrides)
    return AdopterProfile(**defaults)


def make_pet(**overrides):
    defaults = dict(
        id=1,
        name="Test Pet",
        pet_image="/images/test.jpg",
        species=Species.DOG,
        gender=Gender.MALE,
        breed="Mixed",
        age=3,
        energy_level=ActivityLevel.MODERATE,
        apartment_friendly=True,
        experience_required=ExperienceLevel.INTERMEDIATE,
        personality_traits=[],
        good_with_children=True,
        good_with_dogs=True,
        good_with_cats=True,
        notes="",
    )
    defaults.update(overrides)
    return Pet(**defaults)


# --- is_eligible ---


def test_apartment_adopter_excludes_non_apartment_friendly_pet():
    profile = make_profile(housing_type=HousingType.APARTMENT)
    pet = make_pet(apartment_friendly=False)
    assert is_eligible(profile, pet) is False


def test_apartment_adopter_allows_apartment_friendly_pet():
    profile = make_profile(housing_type=HousingType.APARTMENT)
    pet = make_pet(apartment_friendly=True)
    assert is_eligible(profile, pet) is True


def test_house_adopter_allows_non_apartment_friendly_pet():
    profile = make_profile(housing_type=HousingType.HOUSE)
    pet = make_pet(apartment_friendly=False)
    assert is_eligible(profile, pet) is True


def test_household_with_children_excludes_pet_not_good_with_children():
    profile = make_profile(household=[HouseholdMember.CHILDREN])
    pet = make_pet(good_with_children=False)
    assert is_eligible(profile, pet) is False


def test_household_with_dogs_excludes_pet_not_good_with_dogs():
    profile = make_profile(household=[HouseholdMember.DOGS])
    pet = make_pet(good_with_dogs=False)
    assert is_eligible(profile, pet) is False


def test_household_with_cats_excludes_pet_not_good_with_cats():
    profile = make_profile(household=[HouseholdMember.CATS])
    pet = make_pet(good_with_cats=False)
    assert is_eligible(profile, pet) is False


def test_empty_household_ignores_good_with_flags():
    profile = make_profile(household=[])
    pet = make_pet(
        good_with_children=False,
        good_with_dogs=False,
        good_with_cats=False,
    )
    assert is_eligible(profile, pet) is True


def test_pet_failing_one_of_several_household_members_is_excluded():
    profile = make_profile(
        household=[HouseholdMember.CHILDREN, HouseholdMember.DOGS]
    )
    pet = make_pet(good_with_children=True, good_with_dogs=False)
    assert is_eligible(profile, pet) is False


def test_pet_satisfying_every_hard_filter_is_eligible():
    profile = make_profile(
        housing_type=HousingType.APARTMENT,
        household=[HouseholdMember.CHILDREN, HouseholdMember.DOGS, HouseholdMember.CATS],
    )
    pet = make_pet(
        apartment_friendly=True,
        good_with_children=True,
        good_with_dogs=True,
        good_with_cats=True,
    )
    assert is_eligible(profile, pet) is True


# --- age bucketing ---


def test_age_bucket_boundaries():
    assert get_age_bucket(0) == AgePreference.YOUNG
    assert get_age_bucket(2) == AgePreference.YOUNG
    assert get_age_bucket(3) == AgePreference.ADULT
    assert get_age_bucket(7) == AgePreference.ADULT
    assert get_age_bucket(8) == AgePreference.SENIOR
    assert get_age_bucket(15) == AgePreference.SENIOR


# --- age scoring ---


def test_age_no_preference_scores_full_regardless_of_pet_age():
    profile = make_profile(preferred_age=AgePreference.NO_PREFERENCE)
    pet = make_pet(age=12)
    assert calculate_age_score(profile, pet) == 25.0


def test_age_exact_bucket_match_scores_full():
    profile = make_profile(preferred_age=AgePreference.YOUNG)
    pet = make_pet(age=1)
    assert calculate_age_score(profile, pet) == 25.0


def test_age_one_bucket_apart_scores_half():
    profile = make_profile(preferred_age=AgePreference.YOUNG)
    pet = make_pet(age=5)
    assert calculate_age_score(profile, pet) == 12.5


def test_age_two_buckets_apart_scores_zero():
    profile = make_profile(preferred_age=AgePreference.YOUNG)
    pet = make_pet(age=10)
    assert calculate_age_score(profile, pet) == 0.0


# --- activity scoring ---


def test_activity_exact_match_scores_full():
    profile = make_profile(activity_level=ActivityLevel.HIGH)
    pet = make_pet(energy_level=ActivityLevel.HIGH)
    assert calculate_activity_score(profile, pet) == 25.0


def test_activity_one_level_apart_scores_half():
    profile = make_profile(activity_level=ActivityLevel.MODERATE)
    pet = make_pet(energy_level=ActivityLevel.HIGH)
    assert calculate_activity_score(profile, pet) == 12.5


def test_activity_two_levels_apart_scores_zero():
    profile = make_profile(activity_level=ActivityLevel.LOW)
    pet = make_pet(energy_level=ActivityLevel.HIGH)
    assert calculate_activity_score(profile, pet) == 0.0


# --- experience scoring (asymmetric) ---


def test_experience_exact_match_scores_full():
    profile = make_profile(experience_level=ExperienceLevel.INTERMEDIATE)
    pet = make_pet(experience_required=ExperienceLevel.INTERMEDIATE)
    assert calculate_experience_score(profile, pet) == 25.0


def test_experience_adopter_above_requirement_still_scores_full():
    profile = make_profile(experience_level=ExperienceLevel.ADVANCED)
    pet = make_pet(experience_required=ExperienceLevel.BEGINNER)
    assert calculate_experience_score(profile, pet) == 25.0


def test_experience_adopter_one_level_below_requirement_scores_half():
    profile = make_profile(experience_level=ExperienceLevel.INTERMEDIATE)
    pet = make_pet(experience_required=ExperienceLevel.ADVANCED)
    assert calculate_experience_score(profile, pet) == 12.5


def test_experience_adopter_two_levels_below_requirement_scores_zero():
    profile = make_profile(experience_level=ExperienceLevel.BEGINNER)
    pet = make_pet(experience_required=ExperienceLevel.ADVANCED)
    assert calculate_experience_score(profile, pet) == 0.0


# --- trait matching ---


def test_get_matched_traits_returns_intersection_sorted():
    profile = make_profile(
        preferred_traits=[Trait.PLAYFUL, Trait.FRIENDLY, Trait.AFFECTIONATE]
    )
    pet = make_pet(
        personality_traits=[Trait.FRIENDLY, Trait.PLAYFUL, Trait.INDEPENDENT]
    )
    assert get_matched_traits(profile, pet) == [Trait.FRIENDLY, Trait.PLAYFUL]


def test_get_matched_traits_returns_empty_when_no_overlap():
    profile = make_profile(preferred_traits=[Trait.SHY])
    pet = make_pet(personality_traits=[Trait.CONFIDENT])
    assert get_matched_traits(profile, pet) == []


def test_trait_score_empty_preference_scores_full():
    profile = make_profile(preferred_traits=[])
    pet = make_pet(personality_traits=[Trait.FRIENDLY])
    assert calculate_trait_score(profile, pet) == 25.0


def test_trait_score_full_overlap_scores_full():
    profile = make_profile(preferred_traits=[Trait.FRIENDLY, Trait.PLAYFUL])
    pet = make_pet(personality_traits=[Trait.FRIENDLY, Trait.PLAYFUL])
    assert calculate_trait_score(profile, pet) == 25.0


def test_trait_score_partial_overlap_is_proportional():
    profile = make_profile(
        preferred_traits=[Trait.FRIENDLY, Trait.PLAYFUL, Trait.AFFECTIONATE]
    )
    pet = make_pet(
        personality_traits=[Trait.FRIENDLY, Trait.PLAYFUL, Trait.INDEPENDENT]
    )
    # 2 of 3 preferred traits matched -> 2/3 * 25 = 16.7
    assert calculate_trait_score(profile, pet) == 16.7


def test_trait_score_zero_overlap_scores_zero():
    profile = make_profile(preferred_traits=[Trait.SHY])
    pet = make_pet(personality_traits=[Trait.CONFIDENT])
    assert calculate_trait_score(profile, pet) == 0.0


def test_trait_score_duplicate_preferred_traits_do_not_inflate_denominator():
    profile = make_profile(preferred_traits=[Trait.FRIENDLY, Trait.FRIENDLY])
    pet = make_pet(personality_traits=[Trait.FRIENDLY])
    assert calculate_trait_score(profile, pet) == 25.0


# --- total score ---


def test_total_score_perfect_match_is_100():
    profile = make_profile(
        preferred_species=SpeciesPreference.DOG,
        preferred_age=AgePreference.ADULT,
        activity_level=ActivityLevel.MODERATE,
        experience_level=ExperienceLevel.INTERMEDIATE,
        preferred_traits=[Trait.FRIENDLY],
    )
    pet = make_pet(
        species=Species.DOG,
        age=5,
        energy_level=ActivityLevel.MODERATE,
        experience_required=ExperienceLevel.INTERMEDIATE,
        personality_traits=[Trait.FRIENDLY],
    )
    assert calculate_score(profile, pet) == 100.0


def test_total_score_complete_mismatch_is_0():
    profile = make_profile(
        preferred_species=SpeciesPreference.DOG,
        preferred_age=AgePreference.YOUNG,
        activity_level=ActivityLevel.LOW,
        experience_level=ExperienceLevel.BEGINNER,
        preferred_traits=[Trait.SHY],
    )
    pet = make_pet(
        species=Species.CAT,
        age=10,
        energy_level=ActivityLevel.HIGH,
        experience_required=ExperienceLevel.ADVANCED,
        personality_traits=[Trait.CONFIDENT],
    )
    assert calculate_score(profile, pet) == 0.0


def test_total_score_sums_individual_category_scores():
    profile = make_profile(
        preferred_species=SpeciesPreference.DOG,
        preferred_age=AgePreference.YOUNG,
        activity_level=ActivityLevel.MODERATE,
        experience_level=ExperienceLevel.INTERMEDIATE,
        preferred_traits=[Trait.FRIENDLY, Trait.PLAYFUL, Trait.AFFECTIONATE],
    )
    pet = make_pet(
        species=Species.DOG,
        age=5,
        energy_level=ActivityLevel.HIGH,
        experience_required=ExperienceLevel.INTERMEDIATE,
        personality_traits=[Trait.FRIENDLY, Trait.PLAYFUL, Trait.INDEPENDENT],
    )
    expected = (
        calculate_age_score(profile, pet)
        + calculate_activity_score(profile, pet)
        + calculate_experience_score(profile, pet)
        + calculate_trait_score(profile, pet)
    )
    assert calculate_score(profile, pet) == round(expected, 1)


# --- get_matches (orchestration) ---


def test_get_matches_excludes_ineligible_pets():
    profile = make_profile(housing_type=HousingType.APARTMENT)
    eligible_pet = make_pet(id=1, apartment_friendly=True)
    ineligible_pet = make_pet(id=2, apartment_friendly=False)

    matches = get_matches(profile, [eligible_pet, ineligible_pet])

    assert [match.pet.id for match in matches] == [1]


def test_get_matches_returns_empty_list_when_no_pets_eligible():
    profile = make_profile(housing_type=HousingType.APARTMENT)
    pets = [make_pet(id=1, apartment_friendly=False)]

    assert get_matches(profile, pets) == []


def test_get_matches_returns_empty_list_for_empty_pets_input():
    profile = make_profile()

    assert get_matches(profile, []) == []


def test_get_matches_sorts_by_score_descending():
    profile = make_profile(
        preferred_species=SpeciesPreference.DOG,
        activity_level=ActivityLevel.HIGH,
    )
    exact_match = make_pet(id=1, species=Species.DOG, energy_level=ActivityLevel.HIGH)
    partial_match = make_pet(id=2, species=Species.DOG, energy_level=ActivityLevel.MODERATE)
    worst_match = make_pet(id=3, species=Species.DOG, energy_level=ActivityLevel.LOW)

    matches = get_matches(profile, [worst_match, exact_match, partial_match])

    assert [match.pet.id for match in matches] == [1, 2, 3]
    assert matches[0].score >= matches[1].score >= matches[2].score


def test_get_matches_returns_petmatch_with_correct_score_and_matched_traits():
    profile = make_profile(preferred_traits=[Trait.FRIENDLY, Trait.PLAYFUL])
    pet = make_pet(id=1, personality_traits=[Trait.FRIENDLY])

    [match] = get_matches(profile, [pet])

    assert isinstance(match, PetMatch)
    assert match.score == calculate_score(profile, pet)
    assert match.matched_traits == get_matched_traits(profile, pet)
