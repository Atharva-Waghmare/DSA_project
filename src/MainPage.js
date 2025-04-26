import React, { useState } from 'react';
import Navbar from './Navbar';
import MovieRecommendationApp from './MovieRecommendationApp';
import BookRecommendationApp from './BookRecommendationApp';
import AnimeRecommendationApp from './AnimeRecommendationApp';
import './MainPage.css';

const MainPage = () => {
    const [currentPage, setCurrentPage] = useState('main');

    const sections = [
        {
            title: 'Movies & TV Shows',
            description: 'Discover and get recommendations for your next favorite movie or TV show',
            icon: '🎬',
            page: 'movies'
        },
        {
            title: 'Anime',
            description: 'Explore anime recommendations and find your next binge-worthy series',
            icon: '🎌',
            page: 'anime'
        },
        {
            title: 'Books',
            description: 'Find your next great read with personalized book recommendations',
            icon: '📚',
            page: 'books'
        }
    ];

    const handleSectionClick = (page) => {
        if (page) {
            setCurrentPage(page);
        }
    };

    const handleLogoClick = () => {
        setCurrentPage('main');
    };

    if (currentPage === 'movies') {
        return (
            <div className="app-container">
                <MovieRecommendationApp onLogoClick={handleLogoClick} />
            </div>
        );
    }

    if (currentPage === 'anime') {
        return (
            <div className="app-container">
                <AnimeRecommendationApp onLogoClick={handleLogoClick} />
            </div>
        );
    }

    if (currentPage === 'books') {
        return (
            <div className="app-container">
                <BookRecommendationApp onLogoClick={handleLogoClick} />
            </div>
        );
    }

    return (
        <div className="app-container">
            <Navbar onLogoClick={handleLogoClick} />
            <main className="main-page">
                <div className="container">
                    <div className="main-header">
                        <h1>Welcome to Entertainment Hub</h1>
                        <p>Your one-stop destination for entertainment recommendations</p>
                    </div>

                    <div className="sections-container">
                        {sections.map((section, index) => (
                            <div
                                key={index}
                                className="section-card"
                                onClick={() => handleSectionClick(section.page)}
                            >
                                <div className="section-icon">{section.icon}</div>
                                <h2>{section.title}</h2>
                                <p>{section.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default MainPage; 