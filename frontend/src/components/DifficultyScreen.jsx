import React from 'react';
import { colors, buttonStyle, buttonHoverStyle } from '../styles'; // Import shared styles

const difficultyContainerStyle = {
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
  flexDirection: 'column',
  alignItems: 'center',
  gap: '20px',
};

const backButtonStyle = {
  ...buttonStyle,
  backgroundColor: colors.secondary, // Soft orange for contrast
};

const backButtonHoverStyle = {
  backgroundColor: '#C97D5E', // Darker orange on hover
  transform: 'scale(1.05)',
};

function DifficultyScreen({ onSelectDifficulty, onBack }) {
  const difficultyLevels = ['Beginner', 'Intermediate', 'Advanced'];

  return (
    <div style={difficultyContainerStyle}>
      <h1 style={titleStyle}>Choose Difficulty</h1>
      <div style={buttonContainerStyle}>
        {difficultyLevels.map((level) => (
          <button
            key={level}
            style={buttonStyle}
            onMouseOver={(e) => Object.assign(e.target.style, buttonHoverStyle)}
            onMouseOut={(e) => Object.assign(e.target.style, buttonStyle)}
            onClick={() => onSelectDifficulty(level.toLowerCase())}
          >
            {level}
          </button>
        ))}
        <button
          style={backButtonStyle}
          onMouseOver={(e) => Object.assign(e.target.style, backButtonHoverStyle)}
          onMouseOut={(e) => Object.assign(e.target.style, backButtonStyle)}
          onClick={onBack}
        >
          Back
        </button>
      </div>
    </div>
  );
}

export default DifficultyScreen;