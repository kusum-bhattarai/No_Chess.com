import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import AnalysisSidebar from './AnalysisSidebar';
import EvaluationBar from './EvaluationBar';
import { buttonStyle } from '../styles'; 
import { Chess } from 'chess.js';

function ReviewScreen({ reviewData, onBack }) {
  const [moveIndex, setMoveIndex] = useState(0);
  const [board, setBoard] = useState(null);

  useEffect(() => {
    const newBoard = new Chess();

    // Apply moves up to the current index
    reviewData.review_data.slice(0, moveIndex + 1).forEach(reviewMove => {
      newBoard.move(reviewMove.move, { sloppy: true });
    });
    setBoard(newBoard);
  }, [moveIndex, reviewData]);

  const handleNextMove = () => {
    if (moveIndex < reviewData.review_data.length - 1) {
      setMoveIndex(moveIndex + 1);
    }
  };

  const handlePreviousMove = () => {
    if (moveIndex > 0) {
      setMoveIndex(moveIndex - 1);
    }
  };

  const currentMoveData = reviewData.review_data[moveIndex];
  const analysisForSidebar = {
      score: currentMoveData.post_eval.score,
      is_mate: currentMoveData.post_eval.is_mate,
      best_move: currentMoveData.best_move,
      pv: currentMoveData.pv.split(' '),
  };


  if (!board) {
    return <div>Loading...</div>;
  }

  return (
    <div style={reviewScreenStyle}>
       <button onClick={onBack} style={backButtonStyle}>Back to Menu</button>
      <h2>{reviewData.event}</h2>
      <p>{reviewData.white} vs. {reviewData.black} ({reviewData.result})</p>
      <div style={reviewContainerStyle}>
        <EvaluationBar analysis={analysisForSidebar} />
        <div style={boardContainerStyle}>
          <Chessboard position={board.fen()} arePiecesDraggable={false} />
        </div>
        <AnalysisSidebar analysis={analysisForSidebar} />
      </div>
      <div style={navigationStyle}>
        <button style={buttonStyle} onClick={handlePreviousMove} disabled={moveIndex === 0}>Previous</button>
        <span>Move {moveIndex + 1} of {reviewData.review_data.length}: {currentMoveData.move}</span>
        <button style={buttonStyle} onClick={handleNextMove} disabled={moveIndex === reviewData.review_data.length - 1}>Next</button>
      </div>
      <p style={commentStyle}>{currentMoveData.comment}</p>
    </div>
  );
}


// Styles
const reviewScreenStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    padding: '20px',
    color: '#E0E0E0',
  };

  const reviewContainerStyle = {
    display: 'flex',
    gap: '20px',
    alignItems: 'center',
    marginBottom: '20px',
  };

  const boardContainerStyle = {
    width: '60vh',
    maxWidth: '600px',
  };

  const navigationStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
    fontSize: '1.2rem',
  };

  const commentStyle = {
      marginTop: '20px',
      fontStyle: 'italic',
      opacity: 0.8
  }

  const backButtonStyle = {
    ...buttonStyle,
    position: 'absolute',
    top: '20px',
    left: '20px',
};


export default ReviewScreen;