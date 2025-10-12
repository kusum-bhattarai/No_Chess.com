from typing import Dict, List, Optional
import os
import chess
import chess.engine

class StockfishEngine:
    def __init__(self, engine_path: Optional[str] = None, depth: int = 12):
        # Resolve engine binary path from env or default to 'stockfish' in PATH
        if engine_path is None:
            engine_path = os.getenv("STOCKFISH_PATH", "stockfish")
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.board = chess.Board()
        self.depth_limit = chess.engine.Limit(depth=depth)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.quit()

    def set_position(self, uci_moves: List[str]):
        self.board = chess.Board()
        for u in uci_moves:
            self.board.push_uci(u)

    def set_depth(self, depth: int):
        self.depth_limit = chess.engine.Limit(depth=depth)

    def analyze_position(self) -> Dict:
        info = self.engine.analyse(self.board, self.depth_limit)
        pov = info.get("score")
        pv = info.get("pv", [])
        rel = pov.relative if pov else None
        is_mate = bool(rel and rel.is_mate())
        if is_mate:
            score_value = rel.mate()
        else:
            score_value = rel.cp if rel else 0

        return {
            "score": int(score_value or 0),
            "is_mate": is_mate,
            "best_move": pv[0].uci() if pv else None,
            "pv": [m.uci() for m in pv],
            "depth": info.get("depth", None),
        }

    def quit(self):
        try:
            self.engine.quit()
        except Exception:
            pass