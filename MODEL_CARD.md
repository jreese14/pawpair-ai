# PawPair RAG Service Model Card

## Limitations

- Uses OpenAI GPT-4o mini, a lighter model that prioritizes speed over reasoning depth.
- Only generates match-specific explanations based on adopter profile + pet match data provided. Cannot offer guidance on other unanswered details out of scope.
- Explanation quality varies by match score and can sometimes be inconsistent despite prompt

## Biases

- Relies on the accuracy and completeness of input data. Inaccuracies in the JSON pet dataset or incomplete adopter profiles directly affect explanation quality.
- The 14 curated pets represent a limited slice of real adoption scenarios; biases in which breeds/traits are included could influence recommendations.
- OpenAI's model may inherit biases from its training data, potentially reflecting broader societal biases in pet preferences or advice.


## Potential Misuse and Prevention
The RAG system cannot really be misused by users because all the input is through the quiz form which has predetermined quiz options. The system should still disclaim that AI explanations are recommendations, not authoritative pet care advice.

## Surprising Findings from Testing
RAG explanations are tonally inconsistent across all match score ranges. For instance, a 38% pet match received positive encouragement while some 50% matches were discouraging, suggesting the score-aware tone adjustment isn't reliably calibrated despite specific instruction in prompt. Unit tests passed 100%, but human evaluation revealed this UX issue: automated testing catches logic, not consistency in generated tone.

## AI Collaboration During Project
Throughout this project, I used AI as a thinking partner for system design, learning new technologies, and problem-solving. I treated AI as a collaborator to explore ideas, fix bugs, and catch edge cases, but always validated its suggestions and maintained critical judgment. Below are examples of both helpful and flawed suggestions that shaped this system.

### One Helpful AI Suggestion
When the RAG explanation endpoint wasn't rendering on the frontend, AI suggested refactoring from multiple Pydantic model parameters (adopter_profile, pet, matched_traits separately) to a single ExplanationRequest object. With separate parameters, Pydantic couldn't disambiguate how to deserialize the JSON body. A single bundled object made the API contract clear and fixed the frontend integration.


### One Flawed or Incorrect AI Suggestion
Early on, AI suggested adding an adopter priority field (freeform text for what adopters prioritize most in a pet) to personalize explanations. This was a mistake: unbounded user text reaching an LLM prompt creates hallucination and prompt injection risks. You caught this risk later when considering priorities that aren't mentioned in pet match data that RAG uses. The correct approach was to remove priority entirely and personalize using only structured fields (matched_traits, pet notes) and enum-based quiz answers.