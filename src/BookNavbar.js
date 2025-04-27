import React from 'react';
import { BookOpen } from 'lucide-react';
import './BookRecommendationApp.css';

function BookNavbar() {
    return (
        <header className="header">
            <div className="container">
                <div className="header-content">
                    <div className="logo">
                        <BookOpen size={30} className="logo-icon" />
                        <h1 className="logo-text">BookMatchr</h1>
                    </div>
                    <div className="nav-menu">
                        <a href="#" className="nav-link">Home</a>
                        <a href="#" className="nav-link">How It Works</a>
                        <a href="#" className="nav-link">Top Picks</a>
                        <a href="#" className="nav-link">About</a>
                    </div>
                </div>
            </div>
        </header>
    );
}

export default BookNavbar; 