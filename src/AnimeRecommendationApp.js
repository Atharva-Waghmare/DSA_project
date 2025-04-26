import React, { useState } from 'react';
import { Plus, X, Search, AlertCircle, Tv } from 'lucide-react';
import Navbar from './Navbar';
import './AnimeRecommendationApp.css';

function AnimeRecommendationApp({ onLogoClick }) {
    const [animeTitles, setAnimeTitles] = useState([]);
    const [newAnimeTitle, setNewAnimeTitle] = useState('');
    const [isInputError, setIsInputError] = useState(false);
    const [maxAnimesReached, setMaxAnimesReached] = useState(false);

    const [userDetails, setUserDetails] = useState({
        name: '',
        genre: '',
        era: '',
        mood: ''
    });

    const [step, setStep] = useState(1); // 1: Add animes, 2: Add details, 3: Results
    const [isLoading, setIsLoading] = useState(false);
    const [recommendations, setRecommendations] = useState([]);

    // Handle adding a new anime
    const handleAddAnime = () => {
        if (!newAnimeTitle.trim()) {
            setIsInputError(true);
            return;
        }

        if (animeTitles.length >= 5) {
            setMaxAnimesReached(true);
            return;
        }

        setAnimeTitles([...animeTitles, newAnimeTitle.trim()]);
        setNewAnimeTitle('');
        setIsInputError(false);

        if (animeTitles.length === 4) {
            setMaxAnimesReached(true);
        }
    };

    // Handle removing an anime
    const handleRemoveAnime = (index) => {
        const updatedAnimes = [...animeTitles];
        updatedAnimes.splice(index, 1);
        setAnimeTitles(updatedAnimes);
        setMaxAnimesReached(false);
    };

    // Handle input key press (Enter)
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleAddAnime();
        }
    };

    // Handle detail form input changes
    const handleDetailChange = (e) => {
        const { name, value } = e.target;
        setUserDetails({ ...userDetails, [name]: value });
    };

    // Handle continuing to details step
    const handleContinueToDetails = () => {
        if (animeTitles.length > 0) {
            setStep(2);
        } else {
            setIsInputError(true);
        }
    };

    // Mock search function - would connect to backend in real app
    const handleGetRecommendations = () => {
        setIsLoading(true);

        // Simulate API call with timeout
        setTimeout(() => {
            const mockResults = [
                { id: 1, title: "Attack on Titan", studio: "MAPPA", year: 2013, episodes: 87, rating: 4.8, image: "/api/placeholder/300/450" },
                { id: 2, title: "Fullmetal Alchemist: Brotherhood", studio: "Bones", year: 2009, episodes: 64, rating: 4.9, image: "/api/placeholder/300/450" },
                { id: 3, title: "Demon Slayer", studio: "ufotable", year: 2019, episodes: 44, rating: 4.7, image: "/api/placeholder/300/450" },
                { id: 4, title: "One Piece", studio: "Toei Animation", year: 1999, episodes: 1000, rating: 4.8, image: "/api/placeholder/300/450" },
                { id: 5, title: "Violet Evergarden", studio: "Kyoto Animation", year: 2018, episodes: 13, rating: 4.6, image: "/api/placeholder/300/450" }
            ];

            setRecommendations(mockResults);
            setIsLoading(false);
            setStep(3);
        }, 1500);
    };

    // Reset to start over
    const handleStartOver = () => {
        setAnimeTitles([]);
        setNewAnimeTitle('');
        setUserDetails({
            name: '',
            genre: '',
            era: '',
            mood: ''
        });
        setIsInputError(false);
        setMaxAnimesReached(false);
        setStep(1);
        setRecommendations([]);
    };

    return (
        <div className="app-container">
            <Navbar onLogoClick={onLogoClick} />
            {/* Main Content */}
            <main className="main-content">
                {/* Step Indicator */}
                <div className="container">
                    <div className="steps-container">
                        <div className="steps-track">
                            <div className={`step-line ${step >= 1 ? 'active' : ''}`}></div>
                            <div className={`step-circle ${step >= 1 ? 'active' : ''}`}>1</div>
                            <div className={`step-line ${step >= 2 ? 'active' : ''}`}></div>
                            <div className={`step-circle ${step >= 2 ? 'active' : ''}`}>2</div>
                            <div className={`step-line ${step >= 3 ? 'active' : ''}`}></div>
                            <div className={`step-circle ${step >= 3 ? 'active' : ''}`}>3</div>
                            <div className={`step-line ${step >= 3 ? 'active' : ''}`}></div>
                        </div>
                    </div>
                </div>

                {/* Step 1: Add Animes */}
                {step === 1 && (
                    <section className="section">
                        <div className="container">
                            <div className="section-header">
                                <h2 className="section-title">Add Your Favorite Anime</h2>
                                <p className="section-subtitle">Enter up to 5 anime series that you enjoy to receive personalized recommendations.</p>
                            </div>

                            <div className="form-container">
                                {/* Anime input */}
                                <div className="input-group">
                                    <input
                                        type="text"
                                        value={newAnimeTitle}
                                        onChange={(e) => {
                                            setNewAnimeTitle(e.target.value);
                                            setIsInputError(false);
                                        }}
                                        onKeyPress={handleKeyPress}
                                        placeholder="Enter anime title"
                                        className={`text-input ${isInputError ? 'error' : ''}`}
                                        disabled={maxAnimesReached}
                                    />
                                    <button
                                        onClick={handleAddAnime}
                                        disabled={maxAnimesReached}
                                        className="add-button"
                                    >
                                        <Plus size={20} />
                                    </button>
                                </div>

                                {isInputError && (
                                    <div className="error-message">
                                        <AlertCircle size={16} className="error-icon" />
                                        <span>Please enter an anime title</span>
                                    </div>
                                )}

                                {maxAnimesReached && animeTitles.length >= 5 && (
                                    <div className="warning-message">
                                        <AlertCircle size={20} />
                                        <p>Maximum of 5 anime titles reached. Remove one to add more.</p>
                                    </div>
                                )}

                                {/* List of added animes */}
                                <div className="anime-list-container">
                                    <h3 className="anime-list-title">Your Anime ({animeTitles.length}/5)</h3>

                                    {animeTitles.length === 0 ? (
                                        <p className="empty-message">No anime added yet</p>
                                    ) : (
                                        <ul className="anime-list">
                                            {animeTitles.map((anime, index) => (
                                                <li key={index} className="anime-list-item">
                                                    <span>{anime}</span>
                                                    <button
                                                        onClick={() => handleRemoveAnime(index)}
                                                        className="remove-button"
                                                    >
                                                        <X size={18} />
                                                    </button>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>

                                {/* Continue button */}
                                <div className="button-container">
                                    <button
                                        onClick={handleContinueToDetails}
                                        className="primary-button"
                                    >
                                        Continue
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>
                )}

                {/* Step 2: Add Details */}
                {step === 2 && (
                    <section className="section">
                        <div className="container">
                            <div className="section-header">
                                <h2 className="section-title">Add Some Details</h2>
                                <p className="section-subtitle">Help us understand your anime preferences better (optional)</p>
                            </div>

                            <div className="form-container details-form">
                                <div className="form-fields">
                                    <div className="form-field">
                                        <label className="form-label">Your Name</label>
                                        <input
                                            type="text"
                                            name="name"
                                            value={userDetails.name}
                                            onChange={handleDetailChange}
                                            className="text-input"
                                            placeholder="Enter your name"
                                        />
                                    </div>

                                    <div className="form-field">
                                        <label className="form-label">Favorite Genre</label>
                                        <select
                                            name="genre"
                                            value={userDetails.genre}
                                            onChange={handleDetailChange}
                                            className="select-input"
                                        >
                                            <option value="">Select a genre</option>
                                            <option value="action">Action</option>
                                            <option value="adventure">Adventure</option>
                                            <option value="comedy">Comedy</option>
                                            <option value="drama">Drama</option>
                                            <option value="fantasy">Fantasy</option>
                                            <option value="horror">Horror</option>
                                            <option value="isekai">Isekai</option>
                                            <option value="mecha">Mecha</option>
                                            <option value="romance">Romance</option>
                                            <option value="scifi">Sci-Fi</option>
                                            <option value="slice">Slice of Life</option>
                                            <option value="sports">Sports</option>
                                            <option value="supernatural">Supernatural</option>
                                        </select>
                                    </div>

                                    <div className="form-field">
                                        <label className="form-label">Preferred Era</label>
                                        <select
                                            name="era"
                                            value={userDetails.era}
                                            onChange={handleDetailChange}
                                            className="select-input"
                                        >
                                            <option value="">Select an era</option>
                                            <option value="classic">Classic (pre-2000s)</option>
                                            <option value="2000s">2000s</option>
                                            <option value="2010s">2010s</option>
                                            <option value="recent">Recent (2020+)</option>
                                            <option value="any">Any era</option>
                                        </select>
                                    </div>

                                    <div className="form-field">
                                        <label className="form-label">Anime Length Preference</label>
                                        <select
                                            name="mood"
                                            value={userDetails.mood}
                                            onChange={handleDetailChange}
                                            className="select-input"
                                        >
                                            <option value="">How long do you prefer?</option>
                                            <option value="short">Short (1-12 episodes)</option>
                                            <option value="medium">Medium (13-24 episodes)</option>
                                            <option value="long">Long (25-50 episodes)</option>
                                            <option value="very-long">Very long (50+ episodes)</option>
                                            <option value="any">Any length</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="button-group">
                                    <button
                                        onClick={() => setStep(1)}
                                        className="secondary-button"
                                    >
                                        Back
                                    </button>
                                    <button
                                        onClick={handleGetRecommendations}
                                        className="search-button"
                                    >
                                        <span>Get Your Anime</span>
                                        <Search size={18} />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>
                )}

                {/* Step 3: Results */}
                {step === 3 && (
                    <section className="section">
                        <div className="container">
                            {isLoading ? (
                                <div className="loading-container">
                                    <div className="loader"></div>
                                </div>
                            ) : (
                                <>
                                    <div className="section-header">
                                        <h2 className="section-title">Your Personalized Anime Recommendations</h2>
                                        <p className="section-subtitle">Based on your choices, we think you'll love these anime series</p>
                                    </div>

                                    <div className="recommendation-grid">
                                        {recommendations.map((anime) => (
                                            <div key={anime.id} className="anime-card">
                                                <img
                                                    src={anime.image}
                                                    alt={anime.title}
                                                    className="anime-poster"
                                                />
                                                <div className="anime-info">
                                                    <div className="anime-header">
                                                        <h4 className="anime-title">{anime.title}</h4>
                                                        <span className="anime-rating">
                                                            {anime.rating}
                                                        </span>
                                                    </div>
                                                    <p className="anime-studio">{anime.studio}</p>
                                                    <p className="anime-details">{anime.year} • {anime.episodes} episodes</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    <div className="button-container">
                                        <button
                                            onClick={handleStartOver}
                                            className="secondary-button"
                                        >
                                            Start Over
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    </section>
                )}
            </main>

            {/* Footer */}
            <footer className="footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-logo">
                            <Tv size={20} className="logo-icon" />
                            <span className="logo-text">Entertainment Hub</span>
                        </div>
                        <div className="copyright">
                            © 2025 AnimeAdvisor. All rights reserved.
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default AnimeRecommendationApp; 