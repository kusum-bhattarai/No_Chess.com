import pytest
from utils import format_score, format_pv, get_evaluation_bar, get_piece_symbols

def test_format_score():
    assert format_score(100, False) == "1.00"
    assert format_score(-50, False) == "-0.50"
    assert format_score(3, True) == "#3"
    assert format_score(-2, True) == "#2"
    assert format_score(0, False) == "0.00"

def test_format_pv():
    assert format_pv(["e2e4", "e7e5"]) == "e4 e5"
    assert format_pv(["e7e8q"]) == "e8q"
    assert format_pv([]) == ""
    assert format_pv(["a2a3"]) == "a3"

def test_get_evaluation_bar():
    bar = get_evaluation_bar(4, False, 8)
    assert len(bar) == 8
    assert bar.count("█") == 4
    assert bar.count("░") == 4
    assert bar == ["░", "░", "░", "░", "█", "█", "█", "█"]
    assert get_evaluation_bar(8, True, 8) == ["█"] * 8
    assert get_evaluation_bar(0, True, 8) == ["░"] * 8
    assert get_evaluation_bar(10, False, 8) == ["█"] * 8
    assert get_evaluation_bar(-1, False, 8) == ["░"] * 8

def test_get_piece_symbols():
    symbols = get_piece_symbols()
    assert symbols["r"] == "♜ "
    assert symbols["."] == "· "
    custom = {"r": "r ", "P": "P "}
    assert get_piece_symbols(custom)["r"] == "r "
    assert get_piece_symbols(custom)["P"] == "P "
    assert get_piece_symbols(custom)["k"] == "♚ "  # Default fallback