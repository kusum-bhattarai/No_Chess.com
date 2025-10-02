import pytest
import chess
from chess_game import ChessGame

@pytest.fixture
def game():
    return ChessGame()

def test_parse_move_valid(game):
    move = game.parse_move('e2e4')
    assert move.uci() == 'e2e4'

def test_parse_move_invalid(game):
    assert game.parse_move('z2z4') is None

def test_make_move_and_undo(game):
    success = game.make_move('e2e4')
    assert success
    assert len(game.move_history) == 1
    game.undo_move()
    assert len(game.move_history) == 0
    assert game.board.fen() == chess.Board().fen()  # Back to start

def test_load_fen_checkmate():
    # Use a known fool's mate position where black just delivered mate
    checkmate_fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
    game = ChessGame()
    game.load_fen(checkmate_fen)
    result = game.get_game_result()
    assert "Checkmate" in result

def test_get_game_result_draws(game):
    # Use a clear insufficient material position (king vs king)
    game.board.set_fen("8/8/8/8/8/8/8/2kK4 w - - 0 1")
    assert "Insufficient material" in game.get_game_result()

def test_get_state_json(game):
    state = game.get_state_json()
    assert "fen" in state
    assert state["turn"] == "white"
    assert "analysis" in state
    assert isinstance(state["legal_moves"], list)

def test_error_handling():
    game = ChessGame()
    success = game.make_move('invalid')
    assert not success