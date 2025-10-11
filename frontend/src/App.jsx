import { useState } from 'react';
import LandingScreen from './components/LandingScreen';
import DifficultyScreen from './components/DifficultyScreen';
import GameScreen from './components/GameScreen';
import apiClient from './api';
import { AppStyle } from './styles'; 

function App() {
  const [view, setView] = useState('landing');
  const [game, setGame] = useState(null);

  const handleStartGame = async (difficulty) => {
    try {
      console.log(`Requesting new game with difficulty: ${difficulty}`);
      const response = await apiClient.post('/start_game', { mode: difficulty });
      setGame(response.data);
      setView('game');
    } catch (error) {
      console.error("Failed to start game:", error);
      alert("Error: Could not start a new game. Is the backend server running?");
    }
  };

  const renderView = () => {
    switch (view) {
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

  // Use the AppStyle here
  return <div style={AppStyle}>{renderView()}</div>;
}

export default App;