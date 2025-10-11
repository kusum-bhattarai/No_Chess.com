import { useState, useEffect, useRef } from 'react';
import { Chessboard } from 'react-chessboard';
import { colors } from '../styles';
import EvaluationBar from './EvaluationBar';
import AnalysisSidebar from './AnalysisSidebar'; 

// --- Component Styles ---
const gameScreenContainerStyle = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  width: '100vw',
  height: '100vh',
  padding: '2vh',
  boxSizing: 'border-box',
};

const gameAreaStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '20px',
  width: '100%',
  height: '100%',
  maxWidth: '1400px', // Keep a max width for large screens
};

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
  const gameAreaRef = useRef(null);

  useEffect(() => {
    function handleResize() {
      if (gameAreaRef.current) {
        const newSize = gameAreaRef.current.offsetHeight;
        setBoardContainerSize(newSize);
      }
    }

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const squareContainer = {
    width: boardContainerSize,
    height: boardContainerSize,
  };

  return (
    <div style={gameScreenContainerStyle}>
      <div ref={gameAreaRef} style={gameAreaStyle}>
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
            
            {/* Add the new AnalysisSidebar here */}
            <div style={{ height: boardContainerSize }}>
              <AnalysisSidebar analysis={gameData.analysis} />
            </div>
          </>
        )}
      </div>
      <p style={sessionIdStyle}>Session ID: {gameData.session_id}</p>
    </div>
  );
}

export default GameScreen;