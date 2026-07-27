import pytest

from app.enums import Trait
from app.pet_repository import PetRepository
from app.schemas import Pet


@pytest.fixture
def repository():
    return PetRepository()


def test_pets_json_loads_successfully(repository):
    pets = repository.get_all()
    assert len(pets) > 0


def test_every_pet_satisfies_the_schema(repository):
    pets = repository.get_all()
    assert all(isinstance(pet, Pet) for pet in pets)


def test_personality_traits_are_valid_enum_values(repository):
    pets = repository.get_all()
    for pet in pets:
        assert all(isinstance(trait, Trait) for trait in pet.personality_traits)


def test_pet_ids_are_unique(repository):
    pets = repository.get_all()
    ids = [pet.id for pet in pets]
    assert len(ids) == len(set(ids))


def test_get_by_id_returns_matching_pet(repository):
    pets = repository.get_all()
    first_pet = pets[0]
    assert repository.get_by_id(first_pet.id).name == first_pet.name


def test_get_by_id_raises_for_unknown_id(repository):
    with pytest.raises(ValueError):
        repository.get_by_id(999999)
