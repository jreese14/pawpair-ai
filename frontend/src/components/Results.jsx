import { useState, useEffect } from 'react';
import './Results.css';

function Results({ matches, adopterProfile, onRetakeQuiz }) {
    const [expandedId, setExpandedId] = useState(null);

    const [loadingId, setLoadingId] = useState(null);
    const [explanations, setExplanations] = useState({});
    const [typedChars, setTypedChars] = useState({});

    const fetchExplanation = async (petId, match) => {
        if (explanations[petId]) return;
        setLoadingId(petId);
        try {
            const response = await fetch('http://localhost:8000/explanation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    adopter_profile: adopterProfile,
                    pet: match.pet,
                    matched_traits: match.matched_traits,
                    score: match.score
                })
            });
            const data = await response.json();
            setExplanations({ ...explanations, [petId]: data.explanation });
            setTypedChars({ ...typedChars, [petId]: 0 });
        } catch (err) {
            console.error('Error fetching explanation:', err);
        } finally {
            setLoadingId(null);
        }
    };

    useEffect(() => {
        if (expandedId && explanations[expandedId] && (typedChars[expandedId] ?? 0) < explanations[expandedId].length) {
            const interval = setInterval(() => {
                setTypedChars((prev) => ({
                    ...prev,
                    [expandedId]: (prev[expandedId] ?? 0) + 1
                }));
            }, 30);
            return () => clearInterval(interval);
        }
    }, [expandedId, explanations, typedChars]);



    const toggleExpanded = (petId) => {
        setExpandedId(expandedId === petId ? null : petId);
    };

    return (
        <div className="results-container">
            <div className="results-header">
                <h1>Your Top {Math.min(matches.length, 5)} Pet Matches ✨</h1>
                <p>These pets are the best matches for your lifestyle, based on your quiz responses.</p>
                <button className="retake-btn" onClick={onRetakeQuiz}>Retake Quiz</button>
            </div>

            <div className="matches-grid">
                {matches.slice(0, 5).map((match, index) => (
                    <div key={match.pet.id} className="match-card">
                        {/* Rank badge */}
                        <div className="rank-badge">{index + 1}</div>

                        {/* Pet image with score overlay */}
                        <div className="pet-image-container">
                            <img
                                src={`https://picsum.photos/300/300?random=${match.pet.id}`}
                                alt={match.pet.name}
                                className="pet-image"
                                onError={(e) => {
                                    e.target.style.display = 'none';
                                }}
                            />
                            <div className="score-badge">
                                {Math.round(match.score)}% Match
                            </div>
                        </div>

                        {/* Card footer */}
                        <div className="card-footer">
                            <h2>{match.pet.name}</h2>
                            <p className="breed">{match.pet.breed}</p>

                            <p className="pet-details">
                                {match.pet.age} year{match.pet.age !== 1 ? 's' : ''} • {match.pet.gender}
                            </p>

                            {/* Trait badges */}
                            <div className="trait-badges">
                                {/* Matched traits */}
                                {match.matched_traits.map((trait) => (
                                    <span key={trait} className="trait-badge matched">
                                        {trait}
                                    </span>
                                ))}

                                {/* Other important traits */}
                                {match.pet.personality_traits
                                    .filter((t) => !match.matched_traits.includes(t))
                                    .slice(0, 2)
                                    .map((trait) => (
                                        <span key={trait} className="trait-badge">
                                            {trait}
                                        </span>
                                    ))}

                                {/* Household compatibility badges */}
                                {match.pet.good_with_children && (
                                    <span className="trait-badge compat">👧 Good with kids</span>
                                )}
                                {match.pet.good_with_dogs && (
                                    <span className="trait-badge compat">🐶 Good with dogs</span>
                                )}
                                {match.pet.good_with_cats && (
                                    <span className="trait-badge compat">🐱 Good with cats</span>
                                )}
                                {match.pet.apartment_friendly && (
                                    <span className="trait-badge compat">🏢 Apartment friendly</span>
                                )}
                            </div>

                            {/* Expandable explanation section */}
                            <div className="explanation-section">
                                <button
                                    className="explanation-toggle"
                                    onClick={() => {
                                        toggleExpanded(match.pet.id);
                                        fetchExplanation(match.pet.id, match);
                                    }}
                                >
                                    <span>Why {match.pet.name} is a good pick</span>
                                    <span className={`arrow ${expandedId === match.pet.id ? 'open' : ''}`}>
                                        ▼
                                    </span>
                                </button>

                                {expandedId === match.pet.id && (
                                    <div className="explanation-content">
                                        {loadingId === match.pet.id ? (
                                            <p>Generating explanation...</p>
                                        ) : (
                                            <p>{(explanations[match.pet.id] || 'Could not generate explanation.').slice(0, typedChars[match.pet.id] ?? 0)}</p>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

        </div>
    );
}

export default Results;
