from enum import Enum


class Species(str, Enum):
    DOG = "Dog"
    CAT = "Cat"


class SpeciesPreference(str, Enum):
    DOG = "Dog"
    CAT = "Cat"
    NO_PREFERENCE = "No Preference"


class HousingType(str, Enum):
    APARTMENT = "Apartment"
    HOUSE = "House"


class ActivityLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


class AvailableTime(str, Enum):
    LESS_THAN_ONE_HOUR = "Less Than 1 Hour"
    ONE_TO_TWO_HOURS = "1-2 Hours"
    TWO_TO_FOUR_HOURS = "2-4 Hours"
    MORE_THAN_FOUR_HOURS = "More Than 4 Hours"


class ExperienceLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class HouseholdMember(str, Enum):
    CHILDREN = "Children"
    DOGS = "Dogs"
    CATS = "Cats"


class Trait(str, Enum):
    FRIENDLY = "Friendly"
    AFFECTIONATE = "Affectionate"
    PLAYFUL = "Playful"
    INDEPENDENT = "Independent"
    CURIOUS = "Curious"
    GENTLE = "Gentle"
    QUIET = "Quiet"
    SOCIAL = "Social"
    CONFIDENT = "Confident"
    SHY = "Shy"
    LOYAL = "Loyal"
