import React from 'react';
import { colors } from '../styles';

const sidebarStyle = {
  width: '250px', // Fixed width for the sidebar
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  padding: '20px',
  backgroundColor: 'rgba(0, 0, 0, 0.2)',
  borderRadius: '8px',
  boxSizing: 'border-box',
  fontFamily: 'monospace',
  color: colors.text,
};

const titleStyle = {
  fontSize: '1.2rem',
  fontWeight: 'bold',
  marginBottom: '20px',
  textAlign: 'center',
  opacity: 0.8,
};

const infoRowStyle = {
  marginBottom: '15px',
  transition: 'background-color 0.3s ease', // Add for hover
  padding: '5px',
  borderRadius: '4px',
};

const labelStyle = {
  fontSize: '0.9rem',
  opacity: 0.6,
  marginBottom: '5px',
};

const valueStyle = {
  fontSize: '1.1rem',
  fontWeight: 'bold',
};

const scoreStyle = (score) => ({
  ...valueStyle,
  color: score > 50 ? '#86C67C' : score < -50 ? '#D87070' : colors.text,
});

function formatScore(score, is_mate) {
  if (is_mate) {
    return `#${Math.abs(score)}`;
  }
  return (score / 100).toFixed(2);
}

function formatPV(pv) {
  if (!pv || pv.length === 0) return 'N/A';
  return pv.slice(0, 5).join(' '); // Show the first 5 moves of the line
}

function AnalysisSidebar({ analysis }) {
  const { score, is_mate, best_move, pv } = analysis || {};

  return (
    <div style={sidebarStyle}>
      <h2 style={titleStyle}>Analysis</h2>

      <div style={infoRowStyle}>
        <div style={labelStyle}>Evaluation</div>
        <div style={scoreStyle(score)}>{formatScore(score, is_mate)}</div>
      </div>

      <div style={infoRowStyle}>
        <div style={labelStyle}>Best Move</div>
        <div style={valueStyle}>{best_move || 'N/A'}</div>
      </div>

      <div style={infoRowStyle}>
        <div style={labelStyle}>Principal Variation</div>
        <div style={{ ...valueStyle, fontSize: '1rem', wordWrap: 'break-word' }}>
          {formatPV(pv)}
        </div>
      </div>
    </div>
  );
}

export default AnalysisSidebar;