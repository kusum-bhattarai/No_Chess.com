import pytest
import subprocess
from unittest.mock import Mock, patch
from engine import StockfishEngine

@pytest.fixture
def mock_popen():
    mock_process = Mock()
    mock_process.stdin = Mock()
    mock_process.stdout = Mock()
    return mock_process

def test_init_with_validation(mocker):
    # Prevent actual binary checks and process start
    mocker.patch('subprocess.run', return_value=Mock(returncode=0, stdout='Stockfish 17.1 by the Stockfish developers'))
    mock_process = Mock()
    mock_process.stdin = Mock()
    mock_process.stdout = Mock()
    mocker.patch('subprocess.Popen', return_value=mock_process)
    # _wait_for_response is used during init to wait for uci/readyok; no-op it
    mocker.patch.object(StockfishEngine, '_wait_for_response', return_value=None)

    engine = StockfishEngine()
    assert engine.depth == 12  # intermediate default

def test_init_invalid_binary(mocker):
    mocker.patch('subprocess.run', return_value=Mock(returncode=1, stdout='Wrong version'))
    with pytest.raises(OSError, match='Invalid or missing Stockfish'):
        StockfishEngine(executable_path='/invalid/path')

def test_set_position(mocker, mock_popen):
    # Mock binary validation and engine process to avoid launching stockfish
    mocker.patch('subprocess.run', return_value=Mock(returncode=0, stdout='Stockfish 17.1 by the Stockfish developers'))
    mocker.patch('subprocess.Popen', return_value=mock_popen)
    mocker.patch.object(StockfishEngine, '_wait_for_response', return_value=None)
    engine = StockfishEngine()
    engine.set_position(['e2e4', 'e7e5'])
    # engine writes multiple commands during init; ensure the position command was sent
    mock_popen.stdin.write.assert_any_call("position startpos moves e2e4 e7e5\n")

def test_analyze_position(mocker, mock_popen):
    # Mock binary validation and engine process
    mocker.patch('subprocess.run', return_value=Mock(returncode=0, stdout='Stockfish 17.1 by the Stockfish developers'))
    mocker.patch('subprocess.Popen', return_value=mock_popen)
    mocker.patch.object(StockfishEngine, '_wait_for_response', return_value=None)
    mock_popen.stdout.readline.side_effect = [
        "info depth 20 score cp 50 pv e2e4 e7e5",
        "bestmove e2e4"
    ]
    # Make select.select report the mock stdout as ready so _read_line_with_timeout uses readline
    mocker.patch('select.select', return_value=([mock_popen.stdout], [], []))
    engine = StockfishEngine()
    analysis = engine.analyze_position()
    assert analysis["score"] == 50
    assert not analysis["is_mate"]
    assert analysis["pv"] == ["e2e4", "e7e5"]
    assert analysis["best_move"] == "e2e4"

def test_analyze_position_mate(mocker, mock_popen):
    # Mock binary validation and engine process
    mocker.patch('subprocess.run', return_value=Mock(returncode=0, stdout='Stockfish 17.1 by the Stockfish developers'))
    mocker.patch('subprocess.Popen', return_value=mock_popen)
    mocker.patch.object(StockfishEngine, '_wait_for_response', return_value=None)
    mock_popen.stdout.readline.side_effect = [
        "info depth 20 score mate 3 pv e2e4",
        "bestmove e2e4"
    ]
    mocker.patch('select.select', return_value=([mock_popen.stdout], [], []))
    engine = StockfishEngine()
    analysis = engine.analyze_position()
    assert analysis["score"] == 3
    assert analysis["is_mate"]

def test_timeout(mocker, mock_popen):
    # Create an engine instance without running __init__ to test _wait_for_response in isolation
    engine = StockfishEngine.__new__(StockfishEngine)
    engine.engine = mock_popen
    # Simulate no file descriptors ready
    mocker.patch('select.select', return_value=([], [], []))
    with pytest.raises(TimeoutError):
        engine._wait_for_response('test', timeout=1)