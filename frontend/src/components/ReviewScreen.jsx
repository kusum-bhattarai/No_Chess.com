import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import AnalysisSidebar from './AnalysisSidebar';
import EvaluationBar from './EvaluationBar';
import { buttonStyle } from '../styles';
import { Chess } from 'chess.js';

function ReviewScreen({ reviewData, onBack }) {
  const [moveIndex, setMoveIndex] = useState(0);
  const [board, setBoard] = useState(null);

  const hasData = reviewData && Array.isArray(reviewData.review_data) && reviewData.review_data.length > 0;

  useEffect(() => {
    if (!hasData) { setBoard(new Chess()); return; }
    const newBoard = new Chess();
    const upto = Math.min(moveIndex, reviewData.review_data.length - 1);
    for (let i = 0; i <= upto; i++) {
      const mv = reviewData.review_data[i].move; // UCI e.g., e2e4 or e7e8q
      if (!mv || mv.length < 4) continue;
      const from = mv.slice(0, 2);
      const to = mv.slice(2, 4);
      const promo = mv.length > 4 ? mv.slice(4, 5) : undefined;
      newBoard.move({ from, to, promotion: promo || 'q' });
    }
    setBoard(newBoard);
  }, [moveIndex, reviewData, hasData]);

  if (!board) return <div>Loading...</div>;
  if (!hasData) {
    return (
      <div style={reviewScreenStyle}>
        <button onClick={onBack} style={backButtonStyle}>Back to Menu</button>
        <h2>No review data</h2>
        <p>Please upload a valid PGN.</p>
      </div>
    );
  }

  const currentMoveData = reviewData.review_data[moveIndex];
  const analysisForSidebar = currentMoveData
    ? {
        score: currentMoveData.post_eval?.score ?? 0,
        is_mate: currentMoveData.post_eval?.is_mate ?? false,
        best_move: currentMoveData.best_move ?? null,
        pv: (currentMoveData.pv || '').split(' ').filter(Boolean),
      }
    : { score: 0, is_mate: false, best_move: null, pv: [] };

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
        <button style={buttonStyle} onClick={() => setMoveIndex(Math.max(0, moveIndex - 1))} disabled={moveIndex === 0}>Previous</button>
        <span>Move {moveIndex + 1} of {reviewData.review_data.length}: {currentMoveData?.move || '-'}</span>
        <button style={buttonStyle} onClick={() => setMoveIndex(Math.min(reviewData.review_data.length - 1, moveIndex + 1))} disabled={moveIndex === reviewData.review_data.length - 1}>Next</button>
      </div>
      {currentMoveData?.comment && <p style={commentStyle}>{currentMoveData.comment}</p>}
    </div>
  );
}

const reviewScreenStyle = { 
    display:'flex', 
    flexDirection:'column', 
    alignItems:'center', 
    justifyContent:'center', 
    height:'100vh', 
    padding:'20px', 
    color:'#686767ff' };

const reviewContainerStyle = { 
    display:'flex', 
    gap:'20px', 
    alignItems:'center', 
    marginBottom:'20px' };

const boardContainerStyle = { 
    width:'60vh', 
    maxWidth:'600px' };

const navigationStyle = { 
    display:'flex', 
    alignItems:'center', 
    gap:'20px', 
    fontSize:'1.2rem' };

const commentStyle = { 
    marginTop:'20px', 
    fontStyle:'italic', 
    opacity:0.8 };

const backButtonStyle = { 
    ...buttonStyle, 
    position:'absolute', 
    top:'20px', 
    left:'20px' };

export default ReviewScreen;