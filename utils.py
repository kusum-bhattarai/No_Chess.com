def format_score(score, is_mate=False):
    """to convert centipawns score and mate score to more readable format"""
    if is_mate:
        return f"#{score}" if score > 0 else f"#{-score}"
    return f"{score / 100:.2f}"

def format_pv(pv):
    """Convert UCI move list to readable format (e.g., ['e2e4', 'e7e5'] -> 'e4 e5')."""
    return " ".join(move[i:i+2] + move[2:] for i in (0, 2) for move in pv)