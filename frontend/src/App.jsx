// src/App.jsx
import { useState } from 'react';
import LandingScreen from './components/LandingScreen';
import DifficultyScreen from './components/DifficultyScreen'; // 1. Import the new component

function App() {
  const [view, setView] = useState('landing'); // 'landing', 'difficulty', 'game', 'review'

  const handleStartGame = (difficulty) => {
    console.log(`Starting game with difficulty: ${difficulty}`);
    // In the next step, we will call the backend API here.
  };

  const renderView = () => {
    switch (view) {
      // 2. Add the 'difficulty' case
      case 'difficulty':
        return (
          <DifficultyScreen 
            onSelectDifficulty={handleStartGame}
            onBack={() => setView('landing')}
          />
        );
      case 'landing':
      default:
        return (
          <LandingScreen 
            onPlay={() => setView('difficulty')} // 3. Update onPlay to change the view
            onReview={() => console.log("User wants to review")} 
          />
        );
    }
  };

  return (
    <div style={containerStyle}>
      {renderView()}
    </div>
  );
}

const containerStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  height: '100vh',
  backgroundColor: '#302E2B',
  color: 'white',
  fontFamily: 'sans-serif'
};

export default App;