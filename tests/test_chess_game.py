import chess
from collections import deque
from typing import Dict, List, Optional
from backend.ui.terminal_ui import TerminalUI
from backend.utils import get_piece_symbols  

class ChessGame:
    def __init__(self, max_score: int = 500):
        self.board = chess.Board()
        self.move_history = deque()  # Stores (move, fen_before)
        self.current_analysis = {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0}
        self.ui = TerminalUI(max_score)

    def set_analysis(self, analysis: Dict):
        self.current_analysis = analysis

    def display_board(self, clear: bool = True):
        self.ui.display_board(self.board, self.current_analysis, clear)

    def display_analysis(self, analysis: Dict):
        self.ui.display_analysis(self.board, analysis)

    def make_move(self, move_str: str) -> bool:
        try:
            move = self.parse_move(move_str)
            if not move:
                return False
            fen_before = self.board.fen()
            self.board.push(move)
            self.move_history.append((move, fen_before))
            self.display_board()
            return True
        except chess.InvalidMoveError:
            print(f"Illegal move: {move_str}")
            return False
        except ValueError as e:
            print(f"Invalid move format: {move_str} ({e})")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def parse_move(self, move_str: str) -> Optional[chess.Move]:
        try:
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                return move
            else:
                return None
        except ValueError:
            return None

    def undo_move(self) -> bool:
        if not self.move_history:
            print("No moves to undo.")
            return False
        _, fen_before = self.move_history.pop()
        self.board.set_fen(fen_before)
        print("Move undone.")
        self.display_board()
        return True

    def get_legal_moves(self) -> List[str]:
        return [move.uci() for move in self.board.legal_moves]

    def print_legal_moves(self):
        moves = self.get_legal_moves()
        print(f"Legal moves ({len(moves)}):")
        positions = {}
        for move in moves:
            start = move[:2]
            if start not in positions:
                positions[start] = []
            positions[start].append(move[2:])
        symbols = get_piece_symbols()
        for start, ends in positions.items():
            piece = self.board.piece_at(chess.parse_square(start))
            piece_symbol = symbols.get(piece.symbol(), piece.symbol()) if piece else "?"
            print(f"{piece_symbol} {start} → {', '.join(ends)}")

    def get_game_result(self) -> Optional[str]:
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            return f"Checkmate! {winner} wins."
        elif self.board.is_stalemate():
            return "Stalemate! Game is a draw."
        elif self.board.is_insufficient_material():
            return "Insufficient material! Game is a draw."
        elif self.board.can_claim_threefold_repetition():
            return "Threefold repetition! Game is a draw."
        elif self.board.is_seventyfive_moves():
            return "75-move rule! Game is a draw."
        elif self.board.is_fivefold_repetition():
            return "Fivefold repetition! Game is a draw."
        return None

    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    def get_fen(self) -> str:
        return self.board.fen()

    def load_fen(self, fen: str, record_history: bool = False) -> bool:
        try:
            if record_history:
                self.move_history.append((None, self.board.fen()))  # Sentinel for undo
            else:
                self.move_history.clear()
            self.board.set_fen(fen)
            print("Position loaded successfully.")
            self.display_board()
            return True
        except ValueError as e:
            print(f"Invalid FEN: {e}")
            return False

    def get_state_json(self) -> Dict:
        result = self.get_game_result()
        return {
            "fen": self.get_fen(),
            "turn": "white" if self.board.turn else "black",
            "analysis": self.current_analysis,
            "legal_moves": self.get_legal_moves(),
            "game_over": self.is_game_over(),
            "result": result
        }

    def get_move_history_uci(self) -> List[str]:
        return [move.uci() for move, _ in self.move_history]