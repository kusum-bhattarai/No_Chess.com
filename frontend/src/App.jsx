import { useState } from 'react';
import LandingScreen from './components/LandingScreen';
import DifficultyScreen from './components/DifficultyScreen';
import GameScreen from './components/GameScreen'; 
import apiClient from './api'; 

function App() {
  const [view, setView] = useState('landing');
  // Add state to hold the current game data
  const [game, setGame] = useState(null); 

  // Update the handler to call the backend
  const handleStartGame = async (difficulty) => {
    try {
      console.log(`Requesting new game with difficulty: ${difficulty}`);
      const response = await apiClient.post('/start_game', { mode: difficulty });
      setGame(response.data); // Store the game data from the backend
      setView('game'); // Switch to the game view
    } catch (error) {
      console.error("Failed to start game:", error);
      alert("Error: Could not start a new game. Is the backend server running?");
    }
  };

  const renderView = () => {
    switch (view) {
      // 5. Add the 'game' case
      case 'game':
        return <GameScreen gameData={game} />;
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
            onPlay={() => setView('difficulty')}
            onReview={() => console.log("User wants to review")} 
          />
        );
    }
  };

  return <div style={containerStyle}>{renderView()}</div>;
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