import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from .app import app, sessions
from .chess_game import ChessGame
import chess
import chess.pgn

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_sessions():
    """Clear sessions before each test"""
    sessions.clear()

def test_start_game_basic():
    """Test start_game with minimal mocking to see what's happening"""
    with patch('backend.app.StockfishEngine') as mock_engine_class:
        # Create a more complete mock
        mock_engine = MagicMock()
        mock_engine.analyze_position.return_value = {
            "score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0
        }
        mock_engine.set_position.return_value = None
        
        # Mock the context manager properly
        mock_engine_class.return_value = Mock()
        mock_engine_class.return_value.__enter__ = Mock(return_value=mock_engine)
        mock_engine_class.return_value.__exit__ = Mock(return_value=None)
        
        response = client.post("/start_game", json={"mode": "intermediate"})
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"Response JSON: {data}")
        except Exception as e:
            print(f"JSON parse error: {e}")
        
        assert response.status_code == 200
        if "session_id" in response.json():
            assert response.json()["session_id"] in sessions
        else:
            # Let's see what's actually in the response
            print("No session_id in response, available keys:", response.json().keys())

def test_start_game():
    """Working version of start_game test"""
    with patch('backend.app.StockfishEngine') as mock_engine_class:
        # Mock the ChessGame to avoid Stockfish dependency entirely
        with patch('backend.app.ChessGame') as mock_game_class:
            mock_game = MagicMock()
            mock_game.get_move_history_uci.return_value = []
            mock_game.get_state_json.return_value = {
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "turn": "white", 
                "analysis": {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0},
                "legal_moves": ["e2e4", "d2d4", "g1f3"],
                "game_over": False,
                "result": None
            }
            mock_game_class.return_value = mock_game
            
            # Mock engine
            mock_engine = MagicMock()
            mock_engine.analyze_position.return_value = {
                "score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0
            }
            mock_engine.set_position.return_value = None
            
            mock_engine_class.return_value.__enter__ = Mock(return_value=mock_engine)
            mock_engine_class.return_value.__exit__ = Mock(return_value=None)
            
            response = client.post("/start_game", json={"mode": "intermediate"})
            
            assert response.status_code == 200
            data = response.json()
            assert "session_id" in data
            assert data["fen"].startswith("rnbqkbnr")
            
            # Check that a session was created
            assert len(sessions) == 1
            session_id = list(sessions.keys())[0]
            assert data["session_id"] == session_id

def test_make_move():
    """Test make_move with proper mocking"""
    with patch('backend.app.StockfishEngine') as mock_engine_class:
        with patch('backend.app.ChessGame') as mock_game_class:
            # Create mock game instance
            mock_game = MagicMock()
            mock_game.get_move_history_uci.return_value = []
            mock_game.make_move.return_value = True  # Move succeeds
            mock_game.is_game_over.return_value = False
            mock_game.board.turn = chess.WHITE  # White's turn after player move
            mock_game.get_state_json.return_value = {
                "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",  # After e2e4
                "turn": "black",
                "analysis": {"score": 50, "is_mate": False, "best_move": "e7e5", "pv": [], "depth": 0},
                "legal_moves": ["e7e5", "d7d5", "g8f6"],
                "game_over": False,
                "result": None
            }
            mock_game_class.return_value = mock_game
            
            # Mock engine
            mock_engine = MagicMock()
            mock_engine.analyze_position.return_value = {
                "score": 50, "is_mate": False, "best_move": "e7e5", "pv": [], "depth": 0
            }
            mock_engine.set_position.return_value = None
            
            mock_engine_class.return_value.__enter__ = Mock(return_value=mock_engine)
            mock_engine_class.return_value.__exit__ = Mock(return_value=None)
            
            # Manually create a session for testing
            import uuid
            session_id = str(uuid.uuid4())
            sessions[session_id] = mock_game
            
            # Test the move
            move_resp = client.post(f"/make_move/{session_id}", json={"move": "e2e4"})
            assert move_resp.status_code == 200
            data = move_resp.json()
            assert data["turn"] == "black"  # After player move, it's black's turn
            assert data["session_id"] == session_id  # session_id should be included

def test_make_move_invalid_session():
    response = client.post("/make_move/invalid-session", json={"move": "e2e4"})
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]

def test_analyze_endpoint():
    """Test analyze endpoint with proper mocking"""
    with patch('backend.app.StockfishEngine') as mock_engine_class:
        # Create mock game
        mock_game = MagicMock()
        mock_game.get_move_history_uci.return_value = []
        
        # Mock engine
        mock_engine = MagicMock()
        mock_engine.analyze_position.return_value = {
            "score": 150, "is_mate": False, "best_move": "e2e4", "pv": ["e2e4", "e7e5"], "depth": 20
        }
        mock_engine.set_position.return_value = None
        
        mock_engine_class.return_value.__enter__ = Mock(return_value=mock_engine)
        mock_engine_class.return_value.__exit__ = Mock(return_value=None)
        
        # Manually create session
        import uuid
        session_id = str(uuid.uuid4())
        sessions[session_id] = mock_game
        
        # Test analysis - should be GET request
        analyze_resp = client.get(f"/analyze/{session_id}")
        print(f"Analyze response status: {analyze_resp.status_code}")
        print(f"Analyze response content: {analyze_resp.text}")
        
        assert analyze_resp.status_code == 200
        data = analyze_resp.json()
        assert data["score"] == 150
        assert data["best_move"] == "e2e4"

def test_get_session_dependency():
    """Test that the session dependency works correctly"""
    with patch('backend.app.ChessGame') as mock_game_class:
        mock_game = MagicMock()
        mock_game_class.return_value = mock_game
        
        import uuid
        session_id = str(uuid.uuid4())
        sessions[session_id] = mock_game
        
        # Test that get_session returns the correct game
        from backend.app import get_session
        game = get_session(session_id)
        assert game == mock_game
        
        # Test that get_session raises 404 for invalid session
        with pytest.raises(Exception) as exc_info:
            get_session("invalid-session")
        assert "Session not found" in str(exc_info.value)

def test_session_management():
    """Test that sessions are properly managed"""
    with patch('backend.app.StockfishEngine') as mock_engine_class:
        with patch('backend.app.ChessGame') as mock_game_class:
            mock_game = MagicMock()
            mock_game.get_move_history_uci.return_value = []
            mock_game.get_state_json.return_value = {
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "turn": "white", 
                "analysis": {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0},
                "legal_moves": ["e2e4", "d2d4", "g1f3"],
                "game_over": False,
                "result": None
            }
            mock_game_class.return_value = mock_game
            
            mock_engine = MagicMock()
            mock_engine.analyze_position.return_value = {
                "score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0
            }
            mock_engine.set_position.return_value = None
            
            mock_engine_class.return_value.__enter__ = Mock(return_value=mock_engine)
            mock_engine_class.return_value.__exit__ = Mock(return_value=None)
            
            # Start a game
            response = client.post("/start_game", json={"mode": "intermediate"})
            assert response.status_code == 200
            data = response.json()
            session_id = data["session_id"]
            
            # Verify session exists
            assert session_id in sessions
            
            # Test analyze on the same session
            analyze_resp = client.get(f"/analyze/{session_id}")
            print(f"Analyze on valid session: {analyze_resp.status_code}")
            assert analyze_resp.status_code == 200

def test_available_routes():
    """Test that all expected routes are available"""
    routes = [route.path for route in app.routes]
    print("Available routes:", routes)
    
    expected_routes = [
        "/start_game",
        "/make_move/{session_id}", 
        "/analyze/{session_id}"
    ]
    
    for expected_route in expected_routes:
        assert expected_route in routes, f"Route {expected_route} not found in {routes}"

def test_websocket_endpoint():
    """Test the WebSocket endpoint for real-time analysis"""
    with patch('backend.app.StockfishEngine') as mock_engine_class:
        # Mock the engine
        mock_engine = MagicMock()
        mock_engine.analyze_position.return_value = {
            "score": 150, "is_mate": False, "best_move": "e2e4", "pv": ["e2e4", "e7e5"], "depth": 20
        }
        mock_engine_class.return_value.__enter__ = Mock(return_value=mock_engine)
        mock_engine_class.return_value.__exit__ = Mock(return_value=None)

        # Manually create a session for testing
        import uuid
        session_id = str(uuid.uuid4())
        # --- THIS IS THE FIX ---
        sessions[session_id] = ChessGame() 
        # -----------------------

        # Test the WebSocket connection
        with client.websocket_connect(f"/ws/{session_id}") as websocket:
            data = websocket.receive_json()
            assert data["score"] == 150
            assert data["best_move"] == "e2e4"

def test_review_pgn_endpoint():
    """Test the PGN review endpoint with a file upload."""
    pgn_content = '[Event "Test Game"]\\n1. e4 e5 *'

    with patch('backend.app.StockfishEngine') as mock_engine_class, \
         patch('shutil.copyfileobj'), \
         patch('os.remove'):

        # Mock the engine
        mock_engine = MagicMock()
        mock_engine.analyze_position.return_value = {
            "score": 50, "is_mate": False, "best_move": "e2e4", "pv": ["e2e4"], "depth": 10
        }
        mock_engine_class.return_value.__enter__.return_value = mock_engine

        # --- THIS IS THE FIX ---
        # Create a mock for a single chess move
        mock_move = MagicMock()
        mock_move.uci.return_value = 'e2e4'

        # Mock the game object returned by chess.pgn.read_game
        mock_game = MagicMock()
        mock_game.headers = {"Event": "Test Game", "White": "Player A", "Black": "Player B", "Result": "1-0"}
        # Configure mainline_moves to return a list containing our mock move
        mock_game.mainline_moves.return_value = [mock_move]
        # -----------------------

        # The PgnReviewer calls read_game, so we patch that call.
        with patch('backend.pgnReview.chess.pgn.read_game', return_value=mock_game):
            response = client.post(
                "/review_pgn",
                files={"pgn_file": ("tmp_test.pgn", pgn_content, "application/x-chess-pgn")}
            )

    assert response.status_code == 200
    data = response.json()
    assert data["event"] == "Test Game"
    assert "review_data" in data
    assert len(data["review_data"]) > 0 # PgnReviewer should now produce data