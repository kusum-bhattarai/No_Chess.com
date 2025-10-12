import chess
from collections import deque
from typing import Dict, List, Optional
from .ui.terminal_ui import TerminalUI
from .utils import get_piece_symbols

class ChessGame:
    def __init__(self, max_score: int = 500):
        self.board = chess.Board()
        # To store history for undo functionality
        self.move_history = deque()
        # To store current analysis
        self.current_analysis = {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0}
        # UI instance for display
        self.ui = TerminalUI(max_score=max_score)
        # Piece symbols for legal moves print
        self.piece_symbols = get_piece_symbols()

        self.resign_result = None  # e.g., "White resigns. Black wins."

    def resign(self, by_color: str):
        if by_color not in ("white", "black"):
            return False
        if by_color == "white":
            self.resign_result = "White resigns. Black wins."
        else:
            self.resign_result = "Black resigns. White wins."
        return True

    def restart(self):
        self.board = chess.Board()
        self.move_history.clear()
        self.current_analysis = {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0}
        self.resign_result = None
        self.display_board()

    # Sets the analysis data
    def set_analysis(self, analysis: Dict):
        self.current_analysis = analysis

    def display_board(self, clear: bool = True):
        self.ui.display_board(self.board, self.current_analysis, clear)

    def display_game_state(self):
        self.ui.display_game_state(self.board)

    def display_analysis(self, analysis: Dict):
        self.ui.display_analysis(self.board, analysis)

    def make_move(self, move_str: str) -> bool:
        try:
            move = self.parse_move(move_str)
            if not move:
                return False
            previous_fen = self.board.fen()
            self.board.push(move)
            self.move_history.append((move, previous_fen))
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

    def _add_to_history(self, move, previous_fen):
        self.move_history.append((move, previous_fen))

    def get_move_history_uci(self):
        # Some entries (from load_fen with record_history=True) may store
        # a sentinel None for the move. Filter those out to avoid errors.
        return [move.uci() for move, _ in self.move_history if move is not None]

    def undo_move(self):
        if not self.move_history:
            print("No moves to undo.")
            return False

        # Undo the last move and board state
        move, previous_fen = self.move_history.pop()

        # Restore the previous board state
        self.board.set_fen(previous_fen)

        # If the popped entry was a sentinel from load_fen(record_history=True)
        # then move will be None — report a different message in that case.
        if move is None:
            print("Position load undone.")
        else:
            print("Move undone.")

        self.display_board()
        return True

    def get_legal_moves(self):
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

        for start, ends in positions.items():
            piece = self.board.piece_at(chess.parse_square(start))
            piece_symbol = self.piece_symbols.get(piece.symbol(), piece.symbol()) if piece else "?"
            print(f"{piece_symbol} {start} → {', '.join(ends)}")

    def get_game_result(self):
        if self.resign_result:
            return self.resign_result
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            return f"Checkmate! {winner} wins."

        elif self.board.is_stalemate():
            return "Stalemate! Game is a draw."

        elif self.board.is_insufficient_material():
            return "Insufficient material! Game is a draw."

        elif self.board.is_seventyfive_moves():
            return "75-move rule! Game is a draw."

        elif self.board.is_fivefold_repetition():
            return "Fivefold repetition! Game is a draw."

        return None

    def is_game_over(self):
        return self.resign_result is not None or self.board.is_game_over()

    def get_fen(self):
        return self.board.fen()

    def load_fen(self, fen, record_history: bool = False):
        """Load a FEN into the board.

        If record_history is True, the previous board state is pushed onto the
        move history so the load can be undone with `undo_move()`. By default
        the move history is cleared (preserves previous behavior).
        """
        try:
            previous_fen = self.board.fen()
            self.board.set_fen(fen)
            if record_history:
                # Store a sentinel move None together with the previous FEN so undo_move works
                self.move_history.append((None, previous_fen))
            else:
                self.move_history.clear()

            print("Position loaded successfully.")
            self.display_board()
            return True
        except ValueError as e:
            print(f"Invalid FEN: {e}")
            return False

    def get_state_json(self):
        """Return a JSON-serializable dict of the current game state for UI/tests."""
        result = self.get_game_result()
        return {
            "fen": self.get_fen(),
            "turn": "white" if self.board.turn else "black",
            "analysis": self.current_analysis,
            "legal_moves": self.get_legal_moves(),
            "game_over": self.is_game_over(),
            "result": result
        }