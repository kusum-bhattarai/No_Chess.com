export const colors = {
  background: '#F0F4F8', // Soft light blue-gray
  text: '#333333', // Dark gray for readability
  primary: '#368293ff', // Cute teal for buttons/accents
  secondary: '#E39774', // Soft orange for highlights
  boardLight: '#E8F1F2', // Pastel light for board squares
  boardDark: '#A7C4BC', // Pastel green for board squares (cute, nature-inspired)
  evalPositive: '#86C67C', // Green for good scores
  evalNegative: '#D87070', // Red for bad scores
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