function LandingScreen({ onPlay, onReview }) {
  const buttonStyle = {
    padding: '20px 40px',
    fontSize: '1.5rem',
    margin: '0 20px',
    cursor: 'pointer',
    borderRadius: '8px',
    border: 'none',
    backgroundColor: '#504E48',
    color: 'white',
    boxShadow: '0 4px 15px rgba(0,0,0,0.2)'
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>NoChess.com</h1>
      <p style={{ marginBottom: '40px', fontSize: '1.2rem' }}>Choose your mode</p>
      <div>
        <button style={buttonStyle} onClick={onPlay}>
          Play Game
        </button>
        <button style={buttonStyle} onClick={onReview}>
          Review PGN
        </button>
      </div>
    </div>
  );
}

export default LandingScreen;