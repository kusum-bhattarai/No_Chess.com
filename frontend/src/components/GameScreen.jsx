import { useState, useEffect, useRef } from 'react';
import { Chessboard } from 'react-chessboard';
import { colors } from '../styles';
import EvaluationBar from './EvaluationBar';

// --- Component Styles ---
const gameScreenContainerStyle = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  width: '100vw',
  height: '100vh',
  padding: '2vh', // Consistent padding on top and bottom
  boxSizing: 'border-box',
};

const gameAreaStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '20px',
  width: '100%',
  height: '100%', // Fill the padded container
};

// This wrapper will be a perfect square, containing the board
const boardWrapperStyle = {
  position: 'relative',
  width: '100%',
  height: '100%',
};

const sessionIdStyle = {
  paddingTop: '15px',
  fontSize: '0.8rem',
  color: colors.text,
  opacity: 0.5,
  fontFamily: 'monospace',
};

// --- The Component ---
function GameScreen({ gameData }) {
  const [boardContainerSize, setBoardContainerSize] = useState(0);
  const gameAreaRef = useRef(null); // Ref for the main game area

  useEffect(() => {
    function handleResize() {
      if (gameAreaRef.current) {
        // The size of our board container is the available height,
        // which is the most stable dimension.
        const newSize = gameAreaRef.current.offsetHeight;
        setBoardContainerSize(newSize);
      }
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Set initial size

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // We set the width of the board container to be the same as the calculated height
  const squareContainer = {
    width: boardContainerSize,
    height: boardContainerSize,
  };

  return (
    <div style={gameScreenContainerStyle}>
      <div ref={gameAreaRef} style={gameAreaStyle}>
        {/* Render only when size is calculated */}
        {boardContainerSize > 0 && (
          <>
            <div style={{ height: boardContainerSize }}>
              <EvaluationBar analysis={gameData.analysis} />
            </div>

            <div style={squareContainer}>
              <div style={boardWrapperStyle}>
                <Chessboard
                  position={gameData.fen}
                  boardWidth={boardContainerSize}
                  customBoardStyle={{
                    borderRadius: '8px',
                    boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)',
                  }}
                  customDarkSquareStyle={{ backgroundColor: colors.boardDark }}
                  customLightSquareStyle={{ backgroundColor: colors.boardLight }}
                />
              </div>
            </div>
          </>
        )}
      </div>
      <p style={sessionIdStyle}>Session ID: {gameData.session_id}</p>
    </div>
  );
}

export default GameScreen;