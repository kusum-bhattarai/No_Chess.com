import React from 'react';
import { colors, buttonStyle, buttonHoverStyle } from '../styles';

const landingContainerStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100vh',
  textAlign: 'center',
};

const titleStyle = {
  fontSize: '2.5rem',
  marginBottom: '40px',
  color: colors.primary,
};

const buttonContainerStyle = {
  display: 'flex',
  gap: '20px',
};

function LandingScreen({ onPlay, onReview }) {
  return (
    <div style={landingContainerStyle}>
      <h1 style={titleStyle}>Welcome to NoChess.com</h1>
      <div style={buttonContainerStyle}>
        <button
          style={buttonStyle}
          onMouseOver={(e) => Object.assign(e.target.style, buttonHoverStyle)}
          onMouseOut={(e) => Object.assign(e.target.style, buttonStyle)}
          onClick={onPlay}
        >
          Play Game
        </button>
        <button
          style={buttonStyle}
          onMouseOver={(e) => Object.assign(e.target.style, buttonHoverStyle)}
          onMouseOut={(e) => Object.assign(e.target.style, buttonStyle)}
          onClick={onReview}
        >
          Review PGN
        </button>
      </div>
    </div>
  );
}

export default LandingScreen;