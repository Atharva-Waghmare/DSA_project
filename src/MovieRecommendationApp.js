import React, { useState } from 'react';
import { Plus, X, Search, AlertCircle, Film } from 'lucide-react';
import Navbar from './Navbar';
import './MovieRecommendationApp.css';

function MovieRecommendationApp({ onLogoClick }) {
    const [movieNames, setMovieNames] = useState([]);
    const [newMovieName, setNewMovieName] = useState('');
    const [isInputError, setIsInputError] = useState(false);
    const [maxMoviesReached, setMaxMoviesReached] = useState(false);

    const [userDetails, setUserDetails] = useState({
        name: '',
        genre: '',
        era: '',
        mood: ''
    });

    const [step, setStep] = useState(1); // 1: Add movies, 2: Add details, 3: Results
    const [isLoading, setIsLoading] = useState(false);
    const [recommendations, setRecommendations] = useState([]);

    // Handle adding a new movie
    const handleAddMovie = () => {
        if (!newMovieName.trim()) {
            setIsInputError(true);
            return;
        }

        if (movieNames.length >= 5) {
            setMaxMoviesReached(true);
            return;
        }

        setMovieNames([...movieNames, newMovieName.trim()]);
        setNewMovieName('');
        setIsInputError(false);

        if (movieNames.length === 4) {
            setMaxMoviesReached(true);
        }
    };

    // Handle removing a movie
    const handleRemoveMovie = (index) => {
        const updatedMovies = [...movieNames];
        updatedMovies.splice(index, 1);
        setMovieNames(updatedMovies);
        setMaxMoviesReached(false);
    };

    // Handle input key press (Enter)
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleAddMovie();
        }
    };

    // Handle detail form input changes
    const handleDetailChange = (e) => {
        const { name, value } = e.target;
        setUserDetails({ ...userDetails, [name]: value });
    };

    // Handle continuing to details step
    const handleContinueToDetails = () => {
        if (movieNames.length > 0) {
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
                { id: 1, title: "Interstellar", year: 2014, rating: 4.8, image: "/api/placeholder/300/450" },
                { id: 2, title: "The Shawshank Redemption", year: 1994, rating: 4.9, image: "/api/placeholder/300/450" },
                { id: 3, title: "Pulp Fiction", year: 1994, rating: 4.7, image: "/api/placeholder/300/450" },
                { id: 4, title: "The Dark Knight", year: 2008, rating: 4.9, image: "/api/placeholder/300/450" },
                { id: 5, title: "Parasite", year: 2019, rating: 4.8, image: "/api/placeholder/300/450" }
            ];

            setRecommendations(mockResults);
            setIsLoading(false);
            setStep(3);
        }, 1500);
    };

    // Reset to start over
    const handleStartOver = () => {
        setMovieNames([]);
        setNewMovieName('');
        setUserDetails({
            name: '',
            genre: '',
            era: '',
            mood: ''
        });
        setIsInputError(false);
        setMaxMoviesReached(false);
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

                {/* Step 1: Add Movies */}
                {step === 1 && (
                    <section className="section">
                        <div className="container">
                            <div className="section-header">
                                <h2 className="section-title">Add Your Favorite Movies</h2>
                                <p className="section-subtitle">Enter up to 5 movies that you enjoy to receive personalized recommendations.</p>
                            </div>

                            <div className="form-container">
                                {/* Movie input */}
                                <div className="input-group">
                                    <input
                                        type="text"
                                        value={newMovieName}
                                        onChange={(e) => {
                                            setNewMovieName(e.target.value);
                                            setIsInputError(false);
                                        }}
                                        onKeyPress={handleKeyPress}
                                        placeholder="Enter movie title"
                                        className={`text-input ${isInputError ? 'error' : ''}`}
                                        disabled={maxMoviesReached}
                                    />
                                    <button
                                        onClick={handleAddMovie}
                                        disabled={maxMoviesReached}
                                        className="add-button"
                                    >
                                        <Plus size={20} />
                                    </button>
                                </div>

                                {isInputError && (
                                    <div className="error-message">
                                        <AlertCircle size={16} className="error-icon" />
                                        <span>Please enter a movie title</span>
                                    </div>
                                )}

                                {maxMoviesReached && movieNames.length >= 5 && (
                                    <div className="warning-message">
                                        <AlertCircle size={20} />
                                        <p>Maximum of 5 movies reached. Remove a movie to add more.</p>
                                    </div>
                                )}

                                {/* List of added movies */}
                                <div className="movie-list-container">
                                    <h3 className="movie-list-title">Your Movies ({movieNames.length}/5)</h3>

                                    {movieNames.length === 0 ? (
                                        <p className="empty-message">No movies added yet</p>
                                    ) : (
                                        <ul className="movie-list">
                                            {movieNames.map((movie, index) => (
                                                <li key={index} className="movie-list-item">
                                                    <span>{movie}</span>
                                                    <button
                                                        onClick={() => handleRemoveMovie(index)}
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
                                <p className="section-subtitle">Help us understand your preferences better (optional)</p>
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
                                            <option value="comedy">Comedy</option>
                                            <option value="drama">Drama</option>
                                            <option value="sci-fi">Sci-Fi</option>
                                            <option value="horror">Horror</option>
                                            <option value="romance">Romance</option>
                                            <option value="thriller">Thriller</option>
                                            <option value="animated">Animated</option>
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
                                            <option value="classic">Classic (pre-1970s)</option>
                                            <option value="70s-80s">70s-80s</option>
                                            <option value="90s-00s">90s-00s</option>
                                            <option value="modern">Modern (2010s+)</option>
                                            <option value="any">Any era</option>
                                        </select>
                                    </div>

                                    <div className="form-field">
                                        <label className="form-label">Current Mood</label>
                                        <select
                                            name="mood"
                                            value={userDetails.mood}
                                            onChange={handleDetailChange}
                                            className="select-input"
                                        >
                                            <option value="">How are you feeling?</option>
                                            <option value="happy">Happy</option>
                                            <option value="relaxed">Relaxed</option>
                                            <option value="thoughtful">Thoughtful</option>
                                            <option value="excited">Excited</option>
                                            <option value="nostalgic">Nostalgic</option>
                                            <option value="adventurous">Adventurous</option>
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
                                        <span>Get Your Movies</span>
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
                                        <h2 className="section-title">Your Personalized Recommendations</h2>
                                        <p className="section-subtitle">Based on your movie choices, we think you'll love these</p>
                                    </div>

                                    <div className="recommendation-grid">
                                        {recommendations.map((movie) => (
                                            <div key={movie.id} className="movie-card">
                                                <img
                                                    src={movie.image}
                                                    alt={movie.title}
                                                    className="movie-poster"
                                                />
                                                <div className="movie-info">
                                                    <div className="movie-header">
                                                        <h4 className="movie-title">{movie.title}</h4>
                                                        <span className="movie-rating">
                                                            {movie.rating}
                                                        </span>
                                                    </div>
                                                    <p className="movie-year">{movie.year}</p>
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
                            <Film size={20} className="logo-icon" />
                            <span className="logo-text">Entertainment Hub</span>
                        </div>
                        <div className="copyright">
                            © 2025 Entertainment Hub. All rights reserved.
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default MovieRecommendationApp;