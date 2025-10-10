from typing import List, Dict

def format_score(score: int, is_mate: bool = False) -> str:
    """Convert a centipawn or mate score to a readable string.

    Args:
        score: Integer score (centipawns or moves to mate).
        is_mate: If True, score represents moves to mate.

    Returns:
        Formatted string (e.g., '1.00' for centipawns, '#3' for mate).
    """
    if is_mate:
        return f"#{score}" if score > 0 else f"#{-score}"
    return f"{score / 100:.2f}"

def format_pv(pv: List[str]) -> str:
    """Convert a list of UCI moves to a readable format (e.g., ['e2e4'] -> 'e4').

    Args:
        pv: List of UCI moves (e.g., ['e2e4', 'e7e5']).

    Returns:
        Space-separated string of moves (e.g., 'e4 e5').
    """
    return " ".join(move[2:4] + move[4:] for move in pv)

def get_evaluation_bar(streak: int, is_mate: bool = False, height: int = 8) -> List[str]:
    """Generate a vertical ASCII evaluation bar.

    Args:
        streak: Number of filled segments (0 to height).
        is_mate: If True, bar is fully filled (white mate) or empty (black mate).
        height: Bar height (default 8).

    Returns:
        List of ASCII characters ('█' for filled, '░' for empty).
    """
    bar = ["░" for _ in range(height)]
    
    #handle mate from either side
    if is_mate:
        streak = height if streak > 0 else 0
    streak = max(0, min(streak, height))
    
    #fill from the bottom for white's advantage
    for i in range(height - 1, height - 1 - streak, -1):
        if 0 <= i < height:
            bar[i] = "█"
    
    return bar

def get_piece_symbols(custom_symbols: Dict[str, str] = None) -> Dict[str, str]:
    """Return piece symbols for chess board display.

    Args:
        custom_symbols: Optional dict to override default symbols.

    Returns:
        Dict mapping piece characters to Unicode symbols.
    """
    default_symbols = {
        'r': '♜ ', 'n': '♞ ', 'b': '♝ ', 'q': '♛ ', 'k': '♚ ', 'p': '♟ ',
        'R': '♖ ', 'N': '♘ ', 'B': '♗ ', 'Q': '♕ ', 'K': '♔ ', 'P': '♙ ',
        '.': '· '
    }
    symbols = default_symbols.copy()
    if custom_symbols:
        symbols.update(custom_symbols)
    return symbols