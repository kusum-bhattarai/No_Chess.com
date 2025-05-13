def format_score(score, is_mate=False):
    """to convert centipawns score and mate score to more readable format"""
    if is_mate:
        return f"#{score}" if score > 0 else f"#{-score}"
    return f"{score / 100:.2f}"

def format_pv(pv):
    """Convert UCI move list to readable format (e.g., ['e2e4', 'e7e5'] -> 'e4 e5')."""
    return " ".join(move[i:i+2] + move[2:] for i in (0, 2) for move in pv)

def get_evaluation_bar(streak, is_mate=False, height=10):
    """Generate vertical ASCII evaluation bar based on streak size."""
    #intialize the bar
    bar = ["░" for _ in range(height)]
    
    #handle mate from either side
    if is_mate:
        streak = 10 if streak > 0 else 0  #fully filled for white, empty for black
    
    #clamp streak to [0, height]
    streak = max(0, min(streak, height))
    
    #fill from the bottom for white's advantage
    for i in range(height - 1, height - 1 - streak, -1):
        if 0 <= i < height:
            bar[i] = "█"
    
    return bar