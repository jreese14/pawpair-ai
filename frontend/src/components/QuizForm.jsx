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
import { Quiz } from '../models/Quiz';
import { getMatches } from '../services/api';
import './QuizForm.css';



function QuizForm({ onMatchesReceived }) {
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

    const isStepComplete = () => {
        if (step === 0) return formState.name.trim() !== '';
        if (step === 1) return formState.preferred_species !== '';
        if (step === 2) return formState.preferred_age !== '';
        if (step === 3) return formState.housing_type !== '';
        if (step === 4) return formState.experience_level !== '';
        if (step === 5) return formState.activity_level !== '';
        if (step === 6) return formState.available_time !== '';
        if (step === 7) return true; // household is optional
        if (step === 8) return true; // traits are optional
        return false;
    };

    const handleSubmit = () => {
        console.log('Form submitted:', formState);
        const quiz = new Quiz(formState);
        const adopterProfile = quiz.createAdopterProfile();
        getMatches(adopterProfile)
        .then((matches) => onMatchesReceived(matches, adopterProfile))
        .catch((error) => console.error('Error fetching matches:', error));
    };
    return (
        <form>
            <div className="step-counter">
                <span className="step-number">{step + 1}</span>
                <span> / 9</span>
            </div>

            {step === 0 && (
                <>
                    <h3>What's your name?</h3>
                    <input
                        id="name"
                        type="text"
                        value={formState.name}
                        onChange={(event) => setFormState({ ...formState, name: event.target.value })}
                        placeholder="Enter your name"
                    />
                </>
            )}
            {step === 1 && (
                <div className="question-container">
                    <h3>What type of pet do you prefer?</h3>
                    <div className="options-group">
                        {SPECIES_PREFERENCE_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="radio"
                                    id={`species-${option}`}
                                    name="preferred_species"
                                    value={option}
                                    checked={formState.preferred_species === option}
                                    onChange={(event) => setFormState({ ...formState, preferred_species: event.target.value })}
                                />
                                <label htmlFor={`species-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 2 && (
                <div className="question-container">
                    <h3>What is your preferred age range for a pet?</h3>
                    <div className="options-group">
                        {AGE_PREFERENCE_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="radio"
                                    id={`age-${option}`}
                                    name="preferred_age"
                                    value={option}
                                    checked={formState.preferred_age === option}
                                    onChange={(event) => setFormState({ ...formState, preferred_age: event.target.value })}
                                />
                                <label htmlFor={`age-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 3 && (
                <div className="question-container">
                    <h3>What type of home do you live in?</h3>
                    <div className="options-group">
                        {HOUSING_TYPE_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="radio"
                                    id={`housing-${option}`}
                                    name="housing_type"
                                    value={option}
                                    checked={formState.housing_type === option}
                                    onChange={(event) => setFormState({ ...formState, housing_type: event.target.value })}
                                />
                                <label htmlFor={`housing-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 4 && (
                <div className="question-container">
                    <h3>What is your experience level with pets?</h3>
                    <div className="options-group">
                        {EXPERIENCE_LEVEL_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="radio"
                                    id={`experience-${option}`}
                                    name="experience_level"
                                    value={option}
                                    checked={formState.experience_level === option}
                                    onChange={(event) => setFormState({ ...formState, experience_level: event.target.value })}
                                />
                                <label htmlFor={`experience-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 5 && (
                <div className="question-container">
                    <h3>What is your typical activity level?</h3>
                    <div className="options-group">
                        {ACTIVITY_LEVEL_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="radio"
                                    id={`activity-${option}`}
                                    name="activity_level"
                                    value={option}
                                    checked={formState.activity_level === option}
                                    onChange={(event) => setFormState({ ...formState, activity_level: event.target.value })}
                                />
                                <label htmlFor={`activity-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 6 && (
                <div className="question-container">
                    <h3>How many hours per day can you dedicate to your pet's care?</h3>
                    <div className="options-group">
                        {AVAILABLE_TIME_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="radio"
                                    id={`time-${option}`}
                                    name="available_time"
                                    value={option}
                                    checked={formState.available_time === option}
                                    onChange={(event) => setFormState({ ...formState, available_time: event.target.value })}
                                />
                                <label htmlFor={`time-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 7 && (
                <div className="question-container">
                    <h3>Does your household include any of the following?</h3>
                    <div className="options-group">
                        {HOUSEHOLD_MEMBER_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="checkbox"
                                    id={`household-${option}`}
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
                                <label htmlFor={`household-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {step === 8 && (
                <div className="question-container">
                    <h3>What are your preferred pet traits?</h3>
                    <div className="options-group">
                        {TRAIT_OPTIONS.map((option) => (
                            <div key={option} className="option-wrapper">
                                <input
                                    type="checkbox"
                                    id={`trait-${option}`}
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
                                <label htmlFor={`trait-${option}`}>{option}</label>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            <div className="nav-buttons">
                <button type="button" onClick={() => setStep(step - 1)} disabled={step === 0}>
                    Back
                </button>
                {step === 8 ? (
                    <button type="button" onClick={handleSubmit}>
                        Submit
                    </button>
                ) : (
                    <button type="button" onClick={() => setStep(step + 1)} disabled={!isStepComplete()}>
                        Next
                    </button>
                )}
            </div>
        </form>
    )

}

export default QuizForm