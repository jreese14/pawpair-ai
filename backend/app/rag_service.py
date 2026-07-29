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
        prompt = f"""You are a warm and helpful pet adoption advisor. Explain to {adopter_profile.name} why {pet.name} would be a great match for them.
        
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
        1. Use simple, everyday language — no technical jargon
        2. Be warm and encouraging, like talking to a friend
        3. Explain WHY these factors work well together in plain terms
        4. Be concise but detailed — 2-3 sentences that actually explain the match
        5. Mention specific traits and why they matter for their lifestyle
        6. Note any important care needs they should know about
        7. Focus on insight, not just repeating facts
        8. Do NOT mention scores, algorithms, or technical details
        9. Do NOT claim guaranteed success or invent pet facts
        10. Do NOT suggest changing the compatibility score
        
        Write a warm, conversational explanation of why this is a good match:"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()