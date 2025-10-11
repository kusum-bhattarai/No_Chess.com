import { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';

function GameScreen({ gameData }) {
  const [boardWidth, setBoardWidth] = useState(500);

  useEffect(() => {
    function handleResize() {
      const newSize = Math.min(window.innerWidth, window.innerHeight) * 0.8;
      setBoardWidth(newSize);
    }
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div>
      <h2 style={{ textAlign: 'center' }}>Game Started!</h2>
      <Chessboard boardWidth={boardWidth} position={gameData.fen} />
      <p style={{ textAlign: 'center' }}>Session ID: {gameData.session_id}</p>
    </div>
  );
}

export default GameScreen;