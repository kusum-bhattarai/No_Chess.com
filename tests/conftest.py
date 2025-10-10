import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_popen():
    mock_process = Mock()
    mock_process.stdin = Mock()
    mock_process.stdout = Mock()
    return mock_process


@pytest.fixture
def mock_engine_env(mocker, mock_popen):
    """Patch subprocess.run and subprocess.Popen and default engine waits.

    Returns the mock_popen for tests that need to adjust stdout.readline side effects.
    """
    # Pretend stockfish binary exists and reports version
    mocker.patch('subprocess.run', return_value=Mock(returncode=0, stdout='Stockfish 17.1 by the Stockfish developers'))
    # Ensure Popen returns our mock process
    mocker.patch('subprocess.Popen', return_value=mock_popen)
    # During __init__, engine waits for uci/readyok — no-op that in unit tests
    mocker.patch('backend.engine.StockfishEngine._wait_for_response', return_value=None)
    return mock_popen
