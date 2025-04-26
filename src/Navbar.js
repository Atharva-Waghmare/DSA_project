import React from 'react';
import { Film } from 'lucide-react';
import './MovieRecommendationApp.css';

const Navbar = ({ onLogoClick }) => (
    <header className="header">
        <div className="container">
            <div className="header-content">
                <div className="logo" style={{ cursor: onLogoClick ? 'pointer' : 'default' }} onClick={onLogoClick}>
                    <Film className="logo-icon" />
                    <span className="logo-text">Entertainment Hub</span>
                </div>
                <nav className="nav-menu">
                    <a href="#" className="nav-link active">Home</a>
                    <a href="#" className="nav-link">How It Works</a>
                    <a href="#" className="nav-link">Top Picks</a>
                    <a href="#" className="nav-link">About</a>
                </nav>
            </div>
        </div>
    </header>
);

export default Navbar; 