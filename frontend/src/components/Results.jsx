import { useState } from 'react';
import './Results.css';

function Results({ matches }) {
  const [expandedId, setExpandedId] = useState(null);
  const [favoriteIds, setFavoriteIds] = useState(new Set());

  const toggleExpanded = (petId) => {
    setExpandedId(expandedId === petId ? null : petId);
  };

  const toggleFavorite = (petId) => {
    const newFavorites = new Set(favoriteIds);
    if (newFavorites.has(petId)) {
      newFavorites.delete(petId);
    } else {
      newFavorites.add(petId);
    }
    setFavoriteIds(newFavorites);
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h1>Your Top {Math.min(matches.length, 5)} Pet Matches ✨</h1>
        <p>These pets are the best matches for your lifestyle, based on your quiz responses.</p>
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

              {/* Favorite button */}
              <button
                className={`favorite-btn ${favoriteIds.has(match.pet.id) ? 'favorited' : ''}`}
                onClick={() => toggleFavorite(match.pet.id)}
                title="Save to favorites"
              >
                {favoriteIds.has(match.pet.id) ? '♥' : '♡'}
              </button>
            </div>

            {/* Card footer */}
            <div className="card-footer">
              <h2>{match.pet.name}</h2>
              <p className="breed">{match.pet.breed}</p>

              <p className="pet-details">
                {match.pet.age} year{match.pet.age !== 1 ? 's' : ''} • {match.pet.gender}
              </p>

              <p className="pet-description">{match.pet.notes}</p>

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
                {match.pet.apartment_friendly && (
                  <span className="trait-badge compat">🏢 Apartment friendly</span>
                )}
              </div>

              {/* Expandable explanation section */}
              <div className="explanation-section">
                <button
                  className="explanation-toggle"
                  onClick={() => toggleExpanded(match.pet.id)}
                >
                  <span>Why {match.pet.name} is a good pick</span>
                  <span className={`arrow ${expandedId === match.pet.id ? 'open' : ''}`}>
                    ▼
                  </span>
                </button>

                {expandedId === match.pet.id && (
                  <div className="explanation-content">
                    <p>
                      AI-powered explanation coming soon! This will show you personalized
                      reasons why {match.pet.name} is a great match based on your responses.
                    </p>
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
