export const colors = {
    background: '#F0F4F8', // Soft light blue-gray
    text: '#333333', // Dark gray for readability
    primary: '#368293ff', // Cute teal for buttons/accents
    secondary: '#E39774', // Soft orange for highlights
    boardLight: '#E8F1F2', // Pastel light for board squares
    boardDark: '#A7C4BC', // Pastel green for board squares (cute, nature-inspired)
    evalPositive: '#86C67C', // Green for good scores
    evalNegative: '#D87070', // Red for bad scores
    // for eval bar transitions
    evalPositive: '#86C67C',
    evalNegative: '#D87070',
};

export const AppStyle = {
  backgroundColor: colors.background,
  color: colors.text,
  fontFamily: "'Roboto', sans-serif", // Clean, modern font (add via Google Fonts in index.html if needed)
  minHeight: '100vh',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
};

export const buttonStyle = {
  backgroundColor: colors.primary,
  color: '#FFFFFF',
  padding: '12px 24px',
  border: 'none',
  borderRadius: '8px', // Rounded for cuteness
  fontSize: '1.2rem',
  cursor: 'pointer',
  transition: 'background-color 0.3s ease, transform 0.2s ease', // Subtle hover animation
  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)', // Soft shadow
};

export const buttonHoverStyle = {
  backgroundColor: '#4A8C9B', // Darker teal on hover
  transform: 'scale(1.05)', // Slight grow for fun UX
};

export const gameContainerStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100vh',
  padding: '20px',
  boxSizing: 'border-box',
  animation: 'fadeIn 0.5s ease', // Fade-in for whole screen
};

export const gameAreaStyle = {
  display: 'flex',
  alignItems: 'stretch', // Align heights
  gap: '20px',
  maxWidth: '1400px',
  width: '100%',
  height: '80vh', // Limit height to prevent "too big"
};

export const boardContainerStyle = {
  position: 'relative',
  flex: 1, // Grow to fill
  maxWidth: '70vh', // Square, responsive to viewport height
  maxHeight: '70vh',
  borderRadius: '12px', // Rounded for cute
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)', // Soft shadow
  overflow: 'hidden', // Clip board
  backgroundColor: colors.background,
};

export const statusStyle = {
  fontSize: '1.2rem',
  marginBottom: '10px',
  color: colors.primary,
  textAlign: 'center',
};

export const backButtonStyle = {
  ...buttonStyle,
  backgroundColor: colors.secondary,
  marginTop: '20px',
};

export const backButtonHoverStyle = {
  backgroundColor: '#C97D5E',
  transform: 'scale(1.05)',
};

// Keyframe for fade-in
export const fadeIn = `@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }`;