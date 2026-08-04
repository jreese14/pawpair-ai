from openai import OpenAI
import os
from dotenv import load_dotenv

from app.schemas import AdopterProfile, Pet
from app.enums import Trait

class RAGService:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_match_explanation(self, adopter_profile: AdopterProfile, pet: Pet, matched_traits: list[Trait], score: float) -> str:
        prompt = f"""You are a helpful pet adoption advisor. Explain to {adopter_profile.name} how compatible they are with {pet.name}.
        
        Adopter Profile:
        - Name: {adopter_profile.name}
        - Activity level: {adopter_profile.activity_level.value}
        - Housing: {adopter_profile.housing_type.value}
        - Experience with pets: {adopter_profile.experience_level.value}
        - Household includes: {', '.join([h.value for h in adopter_profile.household]) if adopter_profile.household else 'Just adults'}
        
        Pet Details:
        - Name: {pet.name} ({pet.breed}, {pet.age} years old)
        - Energy level: {pet.energy_level.value}
        - Experience needed: {pet.experience_required.value}
        - Apartment friendly: {pet.apartment_friendly}
        - Good with children: {pet.good_with_children}
        - Good with dogs: {pet.good_with_dogs}
        - Good with cats: {pet.good_with_cats}
        - Personality traits: {', '.join([t.value for t in pet.personality_traits])}
        - Notes: {pet.notes}
        
        {pet.name}'s personality traits you were looking for: {', '.join([t.value for t in matched_traits])}
        Compatibility score: {score}%
        
        Guidelines:
        1. Keep it brief — 1-2 sentences maximum
        2. Be honest and match the tone to the compatibility score (high scores: positive; low scores: realistic)
        3. Explain WHY based on specific factors (activity, experience, traits)
        4. Mention specific traits and why they matter for their lifestyle
        5. Note any important care needs they should know about
        6. Use simple, everyday language — no technical jargon
        7. Focus on insight, not just repeating facts
        8. Do NOT mention scores, algorithms, or invent pet facts
        
        Write a brief, honest explanation of why this pet might be a match:"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()