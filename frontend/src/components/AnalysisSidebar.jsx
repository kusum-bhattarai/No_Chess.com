import React from 'react';

function formatScore(analysis) {
  if (!analysis) return '-';
  if (analysis.is_mate) return `M${analysis.score}`;
  if (typeof analysis.score === 'number') return (analysis.score / 100).toFixed(2);
  return '-';
}

export default function AnalysisSidebar({
  analysis,
  onHint,
  onAnalyze,
  onResign,
  onRestart,
  analyzeActive = false,
  hintActive = false,
}) {
  const pvList = Array.isArray(analysis?.pv)
    ? analysis.pv
    : (typeof analysis?.pv === 'string' ? analysis.pv.split(' ') : []);

  return (
    <div style={container}>
      {analysis && (
        <div style={section}>
          <div style={row}>
            <span style={label}>Eval</span>
            <span style={value}>{formatScore(analysis)}</span>
          </div>
          <div style={row}>
            <span style={label}>Best</span>
            <span style={mono}>{analysis?.best_move || '-'}</span>
          </div>
          <div style={{ ...row, alignItems: 'flex-start' }}>
            <span style={label}>PV</span>
            <div style={pvBox}>
              {pvList.length ? pvList.map((m, i) => (
                <span key={i} style={pvMove}>{m}</span>
              )) : <span style={dimmed}>-</span>}
            </div>
          </div>
        </div>
      )}

      <div style={controls}>
        {onHint && (
          <button
            style={{ ...btn, ...(hintActive ? btnActiveAlt : {}) }}
            onClick={onHint}
            aria-pressed={hintActive}
          >
            {hintActive ? 'Hide Hint' : 'Hint'}
          </button>
        )}
        {onAnalyze && (
          <button
            style={{ ...btn, ...(analyzeActive ? btnActive : {}) }}
            onClick={onAnalyze}
            aria-pressed={analyzeActive}
          >
            {analyzeActive ? 'Hide Analysis' : 'Analyze'}
          </button>
        )}
        <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
          {onResign && <button style={{ ...btn, background: '#b91c1c' }} onClick={onResign}>Resign</button>}
          {onRestart && <button style={{ ...btn, background: '#0ea5e9' }} onClick={onRestart}>Restart</button>}
        </div>
      </div>
    </div>
  );
}

const container = {
  width: 300,
  minWidth: 280,
  maxWidth: 340,
  display: 'flex',
  flexDirection: 'column',
  gap: 12,
  color: '#F8FAFC',            // near-white text
};

const section = {
  background: '#111827',       // gray-900
  borderRadius: 10,
  padding: 14,
  border: '1px solid #1f2937', // gray-800
};

const row = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: 10,
};

const label = { color: '#CBD5E1', fontSize: 13 };  // slate-300
const value = { fontWeight: 700, fontSize: 16 };
const mono = { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace', color: '#E5E7EB' };

const pvBox = {
  flex: 1,
  marginLeft: 10,
  display: 'flex',
  flexWrap: 'wrap',
  gap: 6,
};

const pvMove = {
  fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
  background: '#0b1220',
  border: '1px solid #1f2937',
  padding: '2px 6px',
  borderRadius: 6,
  color: '#E5E7EB',
};

const dimmed = { color: '#94A3B8' };

const controls = {
  display: 'flex',
  flexDirection: 'column',
  gap: 8,
  background: '#0b0f1a',
  border: '1px solid #1f2937',
  borderRadius: 10,
  padding: 12,
};

const btn = {
  background: '#374151',       // gray-700
  color: '#F8FAFC',
  border: '1px solid #4b5563',
  borderRadius: 8,
  padding: '9px 12px',
  cursor: 'pointer',
  fontWeight: 600,
  transition: 'background .15s ease, transform .05s ease',
};

const btnActive = {
  background: '#2563EB',       // blue-600 when Analyze active
  borderColor: '#1d4ed8',
};

const btnActiveAlt = {
  background: '#f59e0b',       // amber-500 when Hint active
  borderColor: '#d97706',
};