import pytest
import subprocess
from unittest.mock import Mock, patch
from backend.engine import StockfishEngine  

def test_init_with_validation(mock_engine_env):
    # Using the mock_engine_env fixture prevents launching the real binary
    engine = StockfishEngine()
    assert engine.depth == 12  # intermediate default

def test_init_invalid_binary(mocker):
    # If subprocess.run indicates a bad binary, init should raise
    mocker.patch('subprocess.run', return_value=Mock(returncode=1, stdout='Wrong version'))
    with pytest.raises(OSError, match='Invalid or missing Stockfish'):
        StockfishEngine(executable_path='/invalid/path')

def test_set_position(mock_engine_env):
    mock_popen = mock_engine_env
    engine = StockfishEngine()
    engine.set_position(['e2e4', 'e7e5'])
    # engine writes multiple commands during init; ensure the position command was sent
    mock_popen.stdin.write.assert_any_call("position startpos moves e2e4 e7e5\n")

def test_analyze_position(mock_engine_env):
    mock_popen = mock_engine_env
    mock_popen.stdout.readline.side_effect = [
        "info depth 20 score cp 50 pv e2e4 e7e5",
        "bestmove e2e4"
    ]
    # Make select.select report the mock stdout as ready so _read_line_with_timeout uses readline
    mocker = pytest.MonkeyPatch()
    pytest.monkeypatch = mocker
    pytest.monkeypatch.setattr('select.select', lambda *a, **k: ([mock_popen.stdout], [], []))
    engine = StockfishEngine()
    analysis = engine.analyze_position()
    assert analysis["score"] == 50
    assert not analysis["is_mate"]
    assert analysis["pv"] == ["e2e4", "e7e5"]
    assert analysis["best_move"] == "e2e4"

def test_analyze_position_mate(mock_engine_env):
    mock_popen = mock_engine_env
    mock_popen.stdout.readline.side_effect = [
        "info depth 20 score mate 3 pv e2e4",
        "bestmove e2e4"
    ]
    pytest.monkeypatch.setattr('select.select', lambda *a, **k: ([mock_popen.stdout], [], []))
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