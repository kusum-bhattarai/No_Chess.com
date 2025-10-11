import chess
import chess.engine
from typing import List, Dict

class StockfishEngine:
    def __init__(self, mode: str = "intermediate"):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        except FileNotFoundError:
            raise OSError(
                "Stockfish binary not found in PATH. "
                "Ensure the 'stockfish' package is installed in the Docker image."
            )

        # Configure skill level
        skill_map = {
            "beginner": 5,
            "intermediate": 10,
            "advanced": 20
        }
        skill_level = skill_map.get(mode, 10)
        self.engine.configure({"Skill Level": skill_level})

        # Set analysis depth for this session
        depth_map = {
            "beginner": 8,
            "intermediate": 12,
            "advanced": 16
        }
        depth = depth_map.get(mode, 12)
        self.depth_limit = chess.engine.Limit(depth=depth)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """A dedicated method to properly close the engine process."""
        self.engine.quit()

    def set_position(self, moves: List[str]):
        """Creates a board and plays the given moves to set the position."""
        self.board = chess.Board()
        for move in moves:
            try:
                self.board.push_uci(move)
            except ValueError:
                print(f"Invalid move '{move}' in history, skipping.")

    def analyze_position(self) -> Dict:
        """Analyzes the current board position and returns the results."""
        # The python-chess library handles the analysis loop internally
        info = self.engine.analyse(self.board, self.depth_limit)

        score = info.get("score")
        pv = info.get("pv", [])

        is_mate = score.is_mate()
        if is_mate:
            score_value = score.mate()
        else:
            score_value = score.relative.cp

        return {
            "score": score_value,
            "is_mate": is_mate,
            "best_move": pv[0].uci() if pv else None,
            "pv": [move.uci() for move in pv],
            "depth": info.get("depth"),
        }