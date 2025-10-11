import { useState } from 'react';
import LandingScreen from './components/LandingScreen';
import DifficultyScreen from './components/DifficultyScreen';
import GameScreen from './components/GameScreen';
import PgnUploadModal from './components/PgnUploadModal'; 
import apiClient from './api';
import { AppStyle } from './styles'; 
import ReviewScreen from './components/ReviewScreen';

function App() {
  const [view, setView] = useState('landing');
  const [game, setGame] = useState(null);
  const [showPgnModal, setShowPgnModal] = useState(false);
  const [reviewData, setReviewData] = useState(null); 

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

  const handleMove = async (move) => {
    if (!game) return;

    try {
      const response = await apiClient.post(`/make_move/${game.session_id}`, { move });
      setGame(response.data);
    } catch (error) {
      console.error("Failed to make move:", error);
      alert(`Error: ${error.response?.data?.detail || "Could not make the move."}`);
    }
  };

  const handlePgnUpload = async (formData) => {
    const response = await apiClient.post('/review_pgn', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    setReviewData(response.data);
    setView('review'); // Navigate to review screen
    return response; // For modal success
  };

  const renderView = () => {
    switch (view) {
      case 'game':
        return <GameScreen gameData={game} onMove={handleMove} onBack={() => setView('landing')} />;
      case 'difficulty':
        return (
          <DifficultyScreen
            onSelectDifficulty={handleStartGame}
            onBack={() => setView('landing')}
          />
        );
      case 'review':
        return <ReviewScreen reviewData={reviewData} onBack={() => setView('landing')} />;
      case 'landing':
      default:
        return (
          <LandingScreen
            onPlay={() => setView('difficulty')}
            onReview={() => setShowPgnModal(true)} // Show modal
          />
        );
    }
  };

  return (
    <div style={AppStyle}>
      {renderView()}
      {showPgnModal && (
        <PgnUploadModal
          onClose={() => setShowPgnModal(false)}
          onUpload={handlePgnUpload}
        />
      )}
    </div>
  );
}

export default App;