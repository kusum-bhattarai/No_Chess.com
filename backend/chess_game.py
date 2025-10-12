from typing import List, Dict, Optional
import chess

class ChessGame:
    def __init__(self, user_color_white: bool = True):
        self.board = chess.Board()
        self.user_color_white = user_color_white
        self.last_move: Optional[chess.Move] = None
        self._analysis: Optional[Dict] = None
        self._override_game_over: bool = False
        self._override_result: Optional[str] = None
        self._override_status: Optional[str] = None

    def legal_moves_uci(self) -> List[str]:
        return [m.uci() for m in self.board.legal_moves]

    def apply_uci_move(self, uci: str) -> bool:
        try:
            move = chess.Move.from_uci(uci)
        except ValueError:
            return False
        if move not in self.board.legal_moves:
            return False
        self.board.push(move)
        self.last_move = move
        return True

    def make_move(self, uci: str) -> bool:
        return self.apply_uci_move(uci)

    def get_move_history_uci(self) -> List[str]:
        return [m.uci() for m in self.board.move_stack]

    def set_analysis(self, analysis: Dict):
        self._analysis = analysis

    def fen(self) -> str:
        return self.board.fen()

    def turn_color(self) -> str:
        return "white" if self.board.turn == chess.WHITE else "black"

    def game_status(self) -> Dict:
        if self._override_game_over:
            return {
                "in_check": False,
                "in_checkmate": False,
                "in_stalemate": False,
                "is_draw": False,
                "draw_reason": None,
                "game_over": True,
                "result": self._override_result,
                "status": self._override_status or "Game over",
            }

        status = {
            "in_check": self.board.is_check(),
            "in_checkmate": self.board.is_checkmate(),
            "in_stalemate": self.board.is_stalemate(),
            "is_draw": False,
            "draw_reason": None,
            "game_over": self.board.is_game_over(),
            "result": self.board.result() if self.board.is_game_over() else None,
            "status": None,
        }

        if self.board.is_checkmate():
            status["status"] = "Checkmate"
        elif self.board.is_stalemate():
            status["status"] = "Stalemate"
            status["is_draw"] = True
            status["draw_reason"] = "Stalemate"
        elif self.board.is_fivefold_repetition():
            status["status"] = "Fivefold repetition"
            status["is_draw"] = True
            status["draw_reason"] = "Fivefold repetition"
        elif self.board.can_claim_threefold_repetition() or self.board.is_repetition(3):
            status["status"] = "Threefold repetition"
            status["is_draw"] = True
            status["draw_reason"] = "Threefold repetition"
        elif self.board.is_insufficient_material():
            status["status"] = "Insufficient material"
            status["is_draw"] = True
            status["draw_reason"] = "Insufficient material"
        elif self.board.is_seventyfive_moves():
            status["status"] = "75-move rule"
            status["is_draw"] = True
            status["draw_reason"] = "75-move rule"
        elif self.board.can_claim_fifty_moves():
            status["status"] = "50-move rule (claimable)"
        elif self.board.is_fifty_moves():
            status["status"] = "50-move rule"
            status["is_draw"] = True
            status["draw_reason"] = "50-move rule"
        else:
            status["status"] = "In progress"

        return status

    def get_state_json(self) -> Dict:
        status = self.game_status()
        return {
            "fen": self.fen(),
            "turn": self.turn_color(),
            "legal_moves": self.legal_moves_uci(),
            "analysis": self._analysis,
            "game_over": status["game_over"],
            "result": status["result"],
            "status": status["status"],
            "in_check": status["in_check"],
            "in_checkmate": status["in_checkmate"],
            "in_stalemate": status["in_stalemate"],
            "is_draw": status["is_draw"],
            "draw_reason": status["draw_reason"],
            "last_move": (self.last_move.uci() if self.last_move else None),
        }

    def resign(self, resigning_color: str):
        if self._override_game_over or self.board.is_game_over():
            return
        if resigning_color.lower() == "white":
            self._override_result = "0-1"
        else:
            self._override_result = "1-0"
        self._override_status = "Resignation"
        self._override_game_over = True

    def restart(self):
        self.board = chess.Board()
        self.last_move = None
        self._analysis = None
        self._override_game_over = False
        self._override_result = None
        self._override_status = None