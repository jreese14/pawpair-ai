export class Quiz {
  constructor(responses) {
    this.responses = responses
  }

  createAdopterProfile() {
    return {
      name: this.responses.name.trim(),
      preferred_species: this.responses.preferred_species,
      preferred_age: this.responses.preferred_age,
      housing_type: this.responses.housing_type,
      activity_level: this.responses.activity_level,
      available_time: this.responses.available_time,
      experience_level: this.responses.experience_level,
      preferred_traits: this.responses.preferred_traits,
      household: this.responses.household,
    }
  }
}
