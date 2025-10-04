import pytest
import io
from unittest.mock import Mock, patch
import chess.pgn
from pgnReview import PgnReviewer

@pytest.fixture
def mock_engine():
    engine = Mock()
    engine.analyze_position.return_value = {"score": 0, "is_mate": False, "best_move": "e2e4", "pv": ["e2e4", "e7e5"]}
    return engine

@pytest.fixture
def sample_pgn():
    pgn_str = '[Event "Test"]\n1. e4 e5 1-0'
    return io.StringIO(pgn_str)

def test_perform_review_short(mock_engine, sample_pgn, tmp_path):
    # Write sample to temp file
    pgn_file = tmp_path / "test.pgn"
    pgn_file.write_text(sample_pgn.getvalue())
    reviewer = PgnReviewer(mock_engine)
    data = reviewer.perform_review(str(pgn_file))
    assert len(data) == 2  # 2 moves
    assert "Excellent" in data[0]["comment"]  # Assuming best move matches

def test_blunder_comment(mock_engine, sample_pgn, tmp_path):
    # Mock blunder: post_score drops
    # Write the sample PGN so reviewer can open it
    pgn_file = tmp_path / "test.pgn"
    pgn_file.write_text(sample_pgn.getvalue())

    # Provide a sequence of analyses: for each move we call analyze twice
    # (pre and post). For the first move, make a big drop in score.
    analyses = [
        {"score": 350, "is_mate": False, "best_move": "d2d4", "pv": []},  # pre-move (best move different)
        {"score": -100, "is_mate": False, "best_move": "d2d4", "pv": []},  # post-move (blunder; drop 400)
        # second move pre/post - keep neutral
        {"score": 0, "is_mate": False, "best_move": "e7e5", "pv": []},
        {"score": 0, "is_mate": False, "best_move": "e7e5", "pv": []},
    ]
    mock_engine.analyze_position.side_effect = analyses
    reviewer = PgnReviewer(mock_engine)
    data = reviewer.perform_review(str(pgn_file), pause=False)
    assert any("Blunder" in item["comment"] for item in data)

def test_invalid_pgn(mock_engine, tmp_path):
    invalid_pgn = tmp_path / "invalid.pgn"
    invalid_pgn.write_text("Invalid PGN")
    reviewer = PgnReviewer(mock_engine)
    # Assert no crash, prints error
    from io import StringIO
    import sys
    saved = sys.stdout
    try:
        sys.stdout = StringIO()
        reviewer.perform_review(str(invalid_pgn))
        out = sys.stdout.getvalue()
    finally:
        sys.stdout = saved
    assert "No valid" in out

def test_quick_mode_depth(mock_engine):
    reviewer = PgnReviewer(mock_engine, quick_mode=True)
    assert reviewer.review_depth == 10