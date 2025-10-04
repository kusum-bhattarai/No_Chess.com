import pytest
from unittest.mock import patch
from main import main
from io import StringIO

@pytest.fixture
def arg_parser():
    # Mock argparse for tests
    class Args:
        mode = "intermediate"
        pgn = None
    return Args()

def test_main_no_pgn(arg_parser, monkeypatch):
    monkeypatch.setattr("argparse.ArgumentParser.parse_args", lambda *a, **k: arg_parser)
    monkeypatch.setattr("builtins.input", lambda _: "n")  # Quit early
    monkeypatch.setattr("sys.stdout", StringIO())  # Capture print
    with patch("main.StockfishEngine") as mock_engine, \
         patch("main.ChessGame") as mock_game, \
         patch("main.GameRunner") as mock_runner:
        main()
        mock_engine.assert_called_once_with("intermediate")
        mock_runner.return_value.run.assert_called_once()

def test_main_with_pgn(arg_parser, monkeypatch):
    arg_parser.pgn = "test.pgn"
    monkeypatch.setattr("os.path.exists", lambda x: True)
    monkeypatch.setattr("builtins.input", lambda _: "y")  # Play after PGN
    monkeypatch.setattr("argparse.ArgumentParser.parse_args", lambda *a, **k: arg_parser)
    with patch("main.PgnReviewer") as mock_reviewer, \
         patch("main.StockfishEngine") as mock_engine, \
         patch("main.GameRunner") as mock_runner:
        main()
        mock_reviewer.assert_called_once()
        mock_reviewer.return_value.perform_review.assert_called_once_with("test.pgn")

def test_quit_early(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "quit")
    from unittest.mock import Mock
    from main import GameRunner
    # provide dummy engine and game
    fake_engine = Mock()
    fake_game = Mock()
    with patch("sys.stdout", StringIO()) as mock_stdout:
        runner = GameRunner(fake_engine, fake_game)
        # call process_command directly to simulate quit
        runner.process_command("quit")
        assert "Thanks for playing!" in mock_stdout.getvalue()

def test_invalid_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "invalid")
    from unittest.mock import Mock
    from main import GameRunner
    fake_engine = Mock()
    fake_game = Mock()
    with patch("sys.stdout", StringIO()) as mock_stdout:
        fake_game.make_move.return_value = False
        runner = GameRunner(fake_engine, fake_game)
        # Call process_command with invalid input
        runner.process_command("invalid")
        assert "Invalid move" in mock_stdout.getvalue()