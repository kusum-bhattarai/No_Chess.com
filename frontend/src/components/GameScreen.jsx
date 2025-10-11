import { useState, useEffect, useRef, useMemo } from 'react'; 
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js'; 
import { colors, gameContainerStyle, gameAreaStyle, boardContainerStyle, statusStyle, backButtonStyle, backButtonHoverStyle, fadeIn } from '../styles';
import EvaluationBar from './EvaluationBar';
import AnalysisSidebar from './AnalysisSidebar';

function GameScreen({ gameData, onMove, onBack }) { // Add onBack prop
  const game = useMemo(() => new Chess(), []);
  const [optionSquares, setOptionSquares] = useState({});
  const [boardSize, setBoardSize] = useState(0);
  const [liveAnalysis, setLiveAnalysis] = useState(null);
  const gameAreaRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    try {
      game.load(gameData.fen);
    } catch {
      console.error("Invalid FEN:", gameData.fen);
    }
  }, [game, gameData.fen]);

  useEffect(() => {
    const handleResize = () => {
      if (gameAreaRef.current) {
        const size = Math.min(window.innerHeight * 0.7, window.innerWidth * 0.7); // Responsive square
        setBoardSize(size);
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Live evaluation via WebSocket
  useEffect(() => {
    if (!gameData?.session_id) return;

    const wsUrl = `ws://localhost:8000/ws/${gameData.session_id}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLiveAnalysis(data);
      } catch {
        // ignore parse errors
      }
    };

    ws.onerror = () => {
      // On error, fall back to server-pushed analysis via HTTP when user moves
      // console.warn('WebSocket error');
    };

    ws.onclose = () => {
      // No-op; component unmount or session end
      // console.log('WebSocket closed');
    };

    return () => {
      try {
        ws.close();
      } catch {
        console.debug('WebSocket close failed');
      }
    };
  }, [gameData?.session_id]);

  function showLegalMoves(square) {
    const moves = game.moves({ square, verbose: true });
    if (moves.length === 0) return setOptionSquares({});

    const newSquares = {};
    moves.forEach((move) => {
      newSquares[move.to] = {
        background: game.get(move.to) ? 'radial-gradient(circle, rgba(0,0,0,.1) 85%, transparent 85%)' : 'radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)',
        borderRadius: '50%',
      };
    });
    newSquares[square] = { background: 'rgba(255, 255, 0, 0.4)' };
    setOptionSquares(newSquares);
  }

  function onPieceDrop(source, target) {
    setOptionSquares({});
    if (game.turn() !== gameData.turn[0]) return false;

    const move = game.move({ from: source, to: target, promotion: 'q' });
    if (move === null) return false;

    onMove(`${source}${target}`);
    return true; // Changed to true for successful drop
  }

  const status = gameData.game_over ? gameData.result : `Turn: ${gameData.turn.charAt(0).toUpperCase() + gameData.turn.slice(1)}`;
  const analysis = liveAnalysis || gameData.analysis;

  return (
    <div style={gameContainerStyle}>
      <style>{fadeIn}</style>
      <p style={statusStyle}>{status}</p>
      <div ref={gameAreaRef} style={gameAreaStyle}>
        <EvaluationBar analysis={analysis} />
        <div style={{ ...boardContainerStyle, width: boardSize, height: boardSize }}>
          <Chessboard
            position={gameData.fen}
            boardWidth={boardSize}
            onPieceDrop={onPieceDrop}
            onPieceDragBegin={showLegalMoves}
            onSquareClick={() => setOptionSquares({})}
            customSquareStyles={optionSquares}
            customBoardStyle={{ borderRadius: '8px', boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)' }}
            customDarkSquareStyle={{ backgroundColor: colors.boardDark }}
            customLightSquareStyle={{ backgroundColor: colors.boardLight }}
          />
        </div>
        <AnalysisSidebar analysis={analysis} />
      </div>
      <button
        style={backButtonStyle}
        onMouseOver={(e) => Object.assign(e.target.style, backButtonHoverStyle)}
        onMouseOut={(e) => Object.assign(e.target.style, backButtonStyle)}
        onClick={onBack}
      >
        Back to Menu
      </button>
      <p style={{ fontSize: '0.8rem', color: colors.text, opacity: 0.5, marginTop: '10px' }}>Session ID: {gameData.session_id}</p>
    </div>
  );
}

export default GameScreen;