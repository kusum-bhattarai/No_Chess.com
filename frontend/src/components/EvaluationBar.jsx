import React from 'react';
import { colors } from '../styles';

const barContainerStyle = {
  display: 'flex',
  flexDirection: 'column',
  width: '24px',
  height: '100%',
  backgroundColor: colors.background,
  borderRadius: '4px',
  overflow: 'hidden',
  border: `1px solid ${colors.boardDark}`,
};

const barStyle = {
  width: '100%',
  transition: 'height 0.5s ease-in-out',
};

const whiteBarSyle = {
  ...barStyle,
  backgroundColor: colors.boardLight,
};

const blackBarStyle = {
  ...barStyle,
  backgroundColor: colors.boardDark,
};

// This function converts the engine's score into a percentage for White's advantage.
const calculateWhiteAdvantagePercentage = (analysis) => {
  if (!analysis) return 50; // Default to an equal position

  const { score, is_mate } = analysis;
  const maxScore = 1000; // Represents a +/- 10.00 pawn advantage

  if (is_mate) {
    return score > 0 ? 100 : 0; // If White is mating, 100%. If Black is mating, 0%.
  }

  // Cap the score to our defined max/min for a stable bar
  const cappedScore = Math.max(-maxScore, Math.min(score, maxScore));

  // Convert the score from [-1000, 1000] to a [0, 100] percentage range
  const percentage = ((cappedScore + maxScore) / (2 * maxScore)) * 100;

  return percentage;
};

function EvaluationBar({ analysis }) {
  const whiteHeight = calculateWhiteAdvantagePercentage(analysis);
  const blackHeight = 100 - whiteHeight;

  return (
    <div style={barContainerStyle}>
      {/* Black's advantage bar (grows from the top) */}
      <div style={{ ...blackBarStyle, height: `${blackHeight}%` }}></div>
      {/* White's advantage bar (grows from the bottom) */}
      <div style={{ ...whiteBarSyle, height: `${whiteHeight}%` }}></div>
    </div>
  );
}

export default EvaluationBar;