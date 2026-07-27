import { useState } from 'react';
import {
    SPECIES_PREFERENCE_OPTIONS,
    AGE_PREFERENCE_OPTIONS,
    HOUSING_TYPE_OPTIONS,
    ACTIVITY_LEVEL_OPTIONS,
    AVAILABLE_TIME_OPTIONS,
    EXPERIENCE_LEVEL_OPTIONS,
    HOUSEHOLD_MEMBER_OPTIONS,
    TRAIT_OPTIONS,
} from '../constants/quizOptions';


function QuizForm() {
    const [formState, setFormState] = useState({
        name: '',
        preferred_species: '',
        preferred_age: '',
        housing_type: '',
        activity_level: '',
        available_time: '',
        experience_level: '',
        household: [],
        preferred_traits: [],
    });
    const [step, setStep] = useState(0);
    return (
        <form>

            {step === 0 && (
                <>
                    <label htmlFor="name">What's your name?</label>
                    <input
                        id="name"
                        type="text"
                        value={formState.name}
                        onChange={(event) => setFormState({ ...formState, name: event.target.value })} placeholder="Enter your name"
                    />
                </>
            )}
            {step === 1 && (<div> <h3>What type of pet do you prefer?</h3>
                {SPECIES_PREFERENCE_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="radio"
                                name="preferred_species"
                                value={option}
                                checked={formState.preferred_species === option}
                                onChange={(event) => setFormState({ ...formState, preferred_species: event.target.value })}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 2 && (<div> <h3>What is your preferred age range for a pet?</h3>
                {AGE_PREFERENCE_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="radio"
                                name="preferred_age"
                                value={option}
                                checked={formState.preferred_age === option}
                                onChange={(event) => setFormState({ ...formState, preferred_age: event.target.value })}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 3 && (<div> <h3>What is type of house do you live in?</h3>
                {HOUSING_TYPE_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="radio"
                                name="housing_type"
                                value={option}
                                checked={formState.housing_type === option}
                                onChange={(event) => setFormState({ ...formState, housing_type: event.target.value })}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 4 && (<div> <h3>What is your experience level with pets?</h3>
                {EXPERIENCE_LEVEL_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="radio"
                                name="experience_level"
                                value={option}
                                checked={formState.experience_level === option}
                                onChange={(event) => setFormState({ ...formState, experience_level: event.target.value })}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 5 && (<div> <h3>What is your typical activity level?</h3>
                {ACTIVITY_LEVEL_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="radio"
                                name="activity_level"
                                value={option}
                                checked={formState.activity_level === option}
                                onChange={(event) => setFormState({ ...formState, activity_level: event.target.value })}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 6 && (<div> <h3>How many hours per day can you dedicate to your pet's care?</h3>
                {AVAILABLE_TIME_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="radio"
                                name="available_time"
                                value={option}
                                checked={formState.available_time === option}
                                onChange={(event) => setFormState({ ...formState, available_time: event.target.value })}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 7 && (<div> <h3>Does your household include any of the following?</h3>
                {HOUSEHOLD_MEMBER_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="checkbox"
                                name="household"
                                value={option}
                                checked={formState.household.includes(option)}
                                onChange={() => {
                                    const updated = formState.household.includes(option)
                                        ? formState.household.filter((v) => v !== option)
                                        : [...formState.household, option];
                                    setFormState({ ...formState, household: updated });
                                }}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            {step === 8 && (<div> <h3>What are your preferred pet traits?</h3>
                {TRAIT_OPTIONS.map((option) => (
                    <div key={option}>
                        <label>
                            <input
                                type="checkbox"
                                name="preferred_traits"
                                value={option}
                                checked={formState.preferred_traits.includes(option)}
                                onChange={() => {
                                    const updated = formState.preferred_traits.includes(option)
                                        ? formState.preferred_traits.filter((v) => v !== option)
                                        : [...formState.preferred_traits, option];
                                    setFormState({ ...formState, preferred_traits: updated });
                                }}
                            />
                            {option}
                        </label>
                    </div>
                ))}
            </div>
            )}
            <p>Step: {step}</p>
            <button type="button" onClick={() => setStep(step + 1)}>
                Next
            </button>
            <button type="button" onClick={() => setStep(step - 1)} disabled={step === 0}>
                Back
            </button>
            <pre>{JSON.stringify(formState, null, 2)}</pre>
        </form>
    )

}

export default QuizForm