import { useState, useEffect, useRef, useMemo } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import {
  colors,
  gameContainerStyle,
  gameAreaStyle,
  boardContainerStyle,
  statusStyle,
  backButtonStyle,
  backButtonHoverStyle,
  fadeIn,
} from '../styles';
import EvaluationBar from './EvaluationBar';
import AnalysisSidebar from './AnalysisSidebar';
import apiClient from '../api';

function GameScreen({ gameData, onMove, onBack, onResign, onRestart }) {
  const game = useMemo(() => new Chess(), []);
  const [localFen, setLocalFen] = useState(gameData.fen);
  const [optionSquares, setOptionSquares] = useState({});
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [boardSize, setBoardSize] = useState(560);
  const [liveAnalysis, setLiveAnalysis] = useState(null);       // realtime (eval bar)
  const [manualAnalysis, setManualAnalysis] = useState(null);   // on-demand details (Analyze)
  const [hintArrow, setHintArrow] = useState([]);
  const gameAreaRef = useRef(null);
  const wsRef = useRef(null);

  const userColor = (gameData.user_color || 'white').toLowerCase();
  const orientation = userColor;

  // Sync chess.js and local FEN with server FEN
  useEffect(() => {
    try { game.load(gameData.fen); } catch {}
    setLocalFen(gameData.fen);
    // Reset cosmetics on server update
    setHintArrow([]);
    setSelectedSquare(null);
    setOptionSquares({});
    setManualAnalysis(null); // hide details unless requested again
  }, [gameData.fen, game]);

  // Reset on new session
  useEffect(() => {
    setHintArrow([]);
    setSelectedSquare(null);
    setOptionSquares({});
    setLocalFen(gameData.fen);
    setManualAnalysis(null);
  }, [gameData.session_id]);

  // Responsive board size
  useEffect(() => {
    const handleResize = () => {
      if (gameAreaRef.current) {
        const size = Math.min(window.innerHeight * 0.7, window.innerWidth * 0.7);
        setBoardSize(Math.max(420, Math.floor(size)));
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Live eval via WebSocket (eval bar only)
  useEffect(() => {
    if (!gameData?.session_id) return;
    const wsBase = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';
    const ws = new WebSocket(`${wsBase}/ws/${gameData.session_id}`);
    wsRef.current = ws;
    ws.onmessage = (e) => {
      try { setLiveAnalysis(JSON.parse(e.data)); } catch {}
    };
    return () => { try { ws.close(); } catch {} };
  }, [gameData?.session_id]);

  const isUsersTurn = () => {
    const turn = game.turn(); // 'w' | 'b'
    return (turn === 'w' && userColor === 'white') || (turn === 'b' && userColor === 'black');
  };

  const pieceIsUsers = (piece) => {
    if (!piece) return false;
    const color = piece[0] === 'w' ? 'white' : 'black';
    return color === userColor;
  };

  const calcOptionSquares = (square) => {
    const moves = game.moves({ square, verbose: true });
    if (!moves.length) return {};
    const styles = {};
    moves.forEach((m) => {
      styles[m.to] = {
        background: game.get(m.to)
          ? 'radial-gradient(circle, rgba(0,0,0,.3) 85%, transparent 85%)'
          : 'radial-gradient(circle, rgba(0,0,0,.35) 25%, transparent 25%)',
        borderRadius: '50%',
      };
    });
    styles[square] = { background: 'rgba(255, 215, 0, 0.45)' };
    return styles;
  };

  const handleSquareClick = (square) => {
    if (!isUsersTurn()) return;
    const pieceObj = game.get(square);
    const piece = pieceObj ? (pieceObj.color === 'w' ? 'w' : 'b') + pieceObj.type.toUpperCase() : null;

    if (!selectedSquare) {
      if (!piece || !pieceIsUsers(piece)) return;
      setSelectedSquare(square);
      setOptionSquares(calcOptionSquares(square));
      return;
    }

    if (selectedSquare === square) {
      setSelectedSquare(null);
      setOptionSquares({});
      return;
    }

    const move = game.move({ from: selectedSquare, to: square, promotion: 'q' });
    if (move) {
      setSelectedSquare(null);
      setOptionSquares({});
      setLocalFen(game.fen()); // optimistic
      setHintArrow([]);        // clear hint after user move
      setManualAnalysis(null); // hide stale details
      onMove(`${move.from}${move.to}${move.promotion ? move.promotion : ''}`);
      return;
    }

    if (piece && pieceIsUsers(piece)) {
      setSelectedSquare(square);
      setOptionSquares(calcOptionSquares(square));
    } else {
      setSelectedSquare(null);
      setOptionSquares({});
    }
  };

  const onPieceDragBegin = (sourceSquare, piece) => {
    if (!isUsersTurn() || !pieceIsUsers(piece)) return;
    setSelectedSquare(sourceSquare);
    setOptionSquares(calcOptionSquares(sourceSquare));
  };

  const isDraggablePiece = ({ piece, sourceSquare }) => {
    if (!isUsersTurn()) return false;
    if (!pieceIsUsers(piece)) return false;
    const moves = game.moves({ square: sourceSquare, verbose: true });
    return moves.length > 0;
  };

  const onPieceDrop = (source, target) => {
    if (!isUsersTurn()) return false;
    const move = game.move({ from: source, to: target, promotion: 'q' });
    setSelectedSquare(null);
    setOptionSquares({});
    if (!move) return false;
    setLocalFen(game.fen()); // optimistic
    setHintArrow([]);        // clear hint after user move
    setManualAnalysis(null); // hide stale details
    onMove(`${source}${target}${move.promotion ? move.promotion : ''}`);
    return true;
  };

  const status = gameData.game_over
    ? gameData.result || 'Game over'
    : `Turn: ${gameData.turn?.[0]?.toUpperCase()}${gameData.turn?.slice(1)}`;
  const evalForBar = liveAnalysis || gameData.analysis;

  // Toggleable Hint: click again to clear arrow
  const handleHint = async () => {
    if (hintArrow.length > 0) {
      setHintArrow([]);
      return;
    }
    try {
      const { data } = await apiClient.get(`/analyze/${gameData.session_id}`);
      setLiveAnalysis(data); // keep eval bar fresh
      if (data.best_move) {
        setHintArrow([[data.best_move.slice(0, 2), data.best_move.slice(2, 4), '#f59e0b']]);
      }
    } catch {}
  };

  // Toggleable Analyze: click again to hide details
  const handleAnalyze = async () => {
    if (manualAnalysis) {
      setManualAnalysis(null);
      return;
    }
    try {
      const { data } = await apiClient.get(`/analyze/${gameData.session_id}`);
      setLiveAnalysis(data);    // eval bar
      setManualAnalysis(data);  // show details
      setHintArrow([]);         // clear hint arrow
    } catch {}
  };

  // Backend fallbacks if parent did not provide handlers
  const doResign = onResign || (async () => {
    try { await apiClient.post(`/resign/${gameData.session_id}`); } catch {}
  });

  const doRestart = onRestart || (async () => {
    try {
      await apiClient.post(`/restart/${gameData.session_id}`);
      setHintArrow([]);
      setSelectedSquare(null);
      setOptionSquares({});
      setManualAnalysis(null);
    } catch {}
  });

  return (
    <div style={gameContainerStyle}>
      <style>{fadeIn}</style>
      <p style={statusStyle}>{status}</p>
      <div ref={gameAreaRef} style={gameAreaStyle}>
        <EvaluationBar analysis={evalForBar} />
        <div style={{ ...boardContainerStyle, width: boardSize, height: boardSize }}>
          <Chessboard
            position={localFen}
            boardWidth={Math.max(420, boardSize || 420)}
            orientation={orientation}
            onPieceDrop={onPieceDrop}
            onPieceDragBegin={onPieceDragBegin}
            isDraggablePiece={isDraggablePiece}
            onSquareClick={handleSquareClick}
            customSquareStyles={optionSquares}
            customBoardStyle={{ borderRadius: '8px', boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)' }}
            customDarkSquareStyle={{ backgroundColor: colors.boardDark }}
            customLightSquareStyle={{ backgroundColor: colors.boardLight }}
            customArrows={hintArrow}
          />
        </div>
        <AnalysisSidebar
          analysis={manualAnalysis}           // show details only when Analyze toggled on
          onHint={handleHint}
          onAnalyze={handleAnalyze}
          onResign={doResign}
          onRestart={doRestart}
          analyzeActive={!!manualAnalysis}
          hintActive={hintArrow.length > 0}
        />
      </div>
      <button
        style={backButtonStyle}
        onMouseOver={(e) => Object.assign(e.target.style, backButtonHoverStyle)}
        onMouseOut={(e) => Object.assign(e.target.style, backButtonStyle)}
        onClick={onBack}
      >
        Back to Menu
      </button>
      <p style={{ fontSize: '0.8rem', color: colors.text, opacity: 0.6, marginTop: '10px' }}>
        Session ID: {gameData.session_id}
      </p>
    </div>
  );
}

export default GameScreen;