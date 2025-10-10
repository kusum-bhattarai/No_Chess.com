function DifficultyScreen({ onSelectDifficulty, onBack }) {
  const difficultyLevels = ['Beginner', 'Intermediate', 'Advanced'];

  const buttonStyle = {
    padding: '15px 30px',
    fontSize: '1.2rem',
    margin: '10px',
    cursor: 'pointer',
    borderRadius: '8px',
    border: 'none',
    backgroundColor: '#504E48',
    color: 'white',
    boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
    minWidth: '200px'
  };

  const backButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#767470',
    marginTop: '30px'
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Choose Difficulty</h1>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {difficultyLevels.map((level) => (
          <button 
            key={level} 
            style={buttonStyle} 
            onClick={() => onSelectDifficulty(level.toLowerCase())}
          >
            {level}
          </button>
        ))}
        <button style={backButtonStyle} onClick={onBack}>
          Back
        </button>
      </div>
    </div>
  );
}

export default DifficultyScreen;