import { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { colors } from '../styles'; // Import our new colors

// --- Component Styles ---
const gameScreenStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%',
  height: '100%',
  padding: '20px',
};

const boardWrapperStyle = {
  width: '100%',
  maxWidth: '80vh', // Board will not exceed 80% of the viewport height
  margin: 'auto',
};

const sessionIdStyle = {
  marginTop: '20px',
  fontSize: '1rem',
  color: colors.text,
  opacity: 0.6,
  fontFamily: 'monospace',
};

// --- The Component ---
function GameScreen({ gameData }) {
  const [boardWidth, setBoardWidth] = useState(500);

  // This effect will run when the component mounts and on window resize
  useEffect(() => {
    function handleResize() {
      const display = document.querySelector('.board-wrapper');
      if (display) {
        // Set board size based on the container's width, capped by window height
        const newSize = Math.min(display.offsetWidth, window.innerHeight * 0.8);
        setBoardWidth(newSize);
      }
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Call once to set initial size

    // Cleanup the event listener when the component unmounts
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div style={gameScreenStyle}>
      <div style={boardWrapperStyle} className="board-wrapper">
        <Chessboard
          position={gameData.fen}
          boardWidth={boardWidth}
          customBoardStyle={{
            borderRadius: '8px',
            boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)',
          }}
          customDarkSquareStyle={{ backgroundColor: colors.boardDark }}
          customLightSquareStyle={{ backgroundColor: colors.boardLight }}
        />
      </div>
      <p style={sessionIdStyle}>Session ID: {gameData.session_id}</p>
    </div>
  );
}

export default GameScreen;