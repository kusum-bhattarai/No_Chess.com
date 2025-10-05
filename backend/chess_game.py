import chess
from collections import deque
import os
from .utils import format_score, format_pv, get_evaluation_bar, get_piece_symbols

class ChessGame:

    piece_symbols = {
            'r': '♜ ', 'n': '♞ ', 'b': '♝ ', 'q': '♛ ', 'k': '♚ ', 'p': '♟ ',
            'R': '♖ ', 'N': '♘ ', 'B': '♗ ', 'Q': '♕ ', 'K': '♔ ', 'P': '♙ ',
            '.': '· '
        }

    def __init__(self):
        self.board = chess.Board()
        
        #to store history for undo functionality
        self.move_history = deque()
        
        #to store current analysis
        self.current_analysis = {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0}

        #get piece symbols
        self.piece_symbols = get_piece_symbols()
    
    #sets the analysis data
    def set_analysis(self, analysis):
        self.current_analysis = analysis

    def clear_screen(self):
        os.system('clear')

    def display_board(self, clear=True):
        if clear:
            self.clear_screen()

        bar_height = 8  #same as chess board height

        # Get evaluation data
        score = self.current_analysis["score"]
        is_mate = self.current_analysis["is_mate"]

        if is_mate:
            streak = bar_height if score > 0 else 0  #full for white mate, empty for black
        else:
            #converting the score at bar level   
            max_score = 500               
            
            capped_score = max(min(score, max_score), -max_score) #capped at +/-500
            
            #map from [-max_score, max_score] to [0, bar_height]
            streak = int((capped_score + max_score) * bar_height / (2 * max_score))
        
        #get the evaluation bar
        eval_bar = get_evaluation_bar(streak, is_mate, bar_height)
        
        #evaluation score as text
        score_text = format_score(score, is_mate)

        print("            a  b  c  d  e  f  g  h")
        print("          +------------------------+")
        for rank in range(7, -1, -1):
            #evaluation bar segment 
            bar_segment = eval_bar[7 - rank]  # Invert rank for bar alignment

            if rank == 4:  
                #score near the bar
                print(f"{bar_segment} {score_text} | {rank+1}|", end=" ")
            else:
                #consistent spacing for alignment
                print(f"{bar_segment}      | {rank+1}|", end=" ")

            for file in range(8):
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    print(self.piece_symbols[piece.symbol()], end=" ")
                else:
                    print(self.piece_symbols['.'], end=" ")
            print(f"|{rank+1}")
        print("          +------------------------+")
        print("            a  b  c  d  e  f  g  h")
        
        #for current state info
        self.display_game_state()

    def display_game_state(self):
        #display turns
        turn = "White" if self.board.turn else "Black"
        print(f"\nCurrent turn: {turn}")
        
        #special board conditions
        if self.board.is_checkmate():
            print("Checkmate! Game over.")
        elif self.board.is_stalemate():
            print("Stalemate! Game over.")
        elif self.board.is_insufficient_material():
            print("Insufficient material! Game over.")
        elif self.board.is_check():
            print("Check!")

        print(f"Moves played: {len(self.move_history)}")

    def display_analysis(self, analysis):
        """Display Stockfish analysis including score, best move, PV, and insights."""
        score = analysis["score"]
        is_mate = analysis["is_mate"]
        best_move = analysis["best_move"]
        pv = analysis["pv"]
        depth = analysis["depth"]

        #format the analysis
        score_str = format_score(score, is_mate)
        pv_str = format_pv(pv[:4])  #limited pv to 4 which gives sequence of 8 (4 moves each)

        #formatted analysis
        if is_mate:
            insight = f"{'White' if score > 0 else 'Black'} can deliver checkmate in {abs(score)} move(s)."
        else:
            if abs(score) < 50:
                insight = "The position is roughly equal."
            elif score > 0:
                insight = f"White has a {'slight' if score < 200 else 'strong'} advantage."
            else:
                insight = f"Black has a {'slight' if score > -200 else 'strong'} advantage."

        self.display_board(clear=True)

        #display analysis
        print("\nStockfish Analysis:")
        print(f"Depth: {depth}")
        print(f"Evaluation: {score_str}")
        print(f"Best move: {best_move[:2]}{best_move[2:]}")
        print(f"Line: {pv_str}")
        print(f"Position: {insight}")

    def make_move(self, move_str):
        move = self.parse_move(move_str)

        if not move:
            return False
        
        board_copy = self.board.copy()
        self.board.push(move)
        self._add_to_history(move, board_copy)

        self.display_board()
        return True
    
    #to handle move validity
    def parse_move(self, move_str):
        try:
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                return move
            else:
                print(f"Illegal move: {move_str}")
                return None
        except ValueError:
            print(f"Invalid move format: {move_str}")
            return None
        
    def _add_to_history(self, move, previous_board):
        self.move_history.append((move, previous_board))

    def get_move_history_uci(self):
        # Some entries (from load_fen with record_history=True) may store
        # a sentinel None for the move. Filter those out to avoid errors.
        return [move.uci() for move, _ in self.move_history if move is not None]

    def undo_move(self):
        if not self.move_history:
            print("No moves to undo.")
            return False
            
        #undo the last move and board state
        move, previous_board = self.move_history.pop()

        # restore the previous board state
        self.board = previous_board

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
        return self.board.is_game_over()

    def get_fen(self):
        return self.board.fen()

    def load_fen(self, fen, record_history: bool = False):
        """Load a FEN into the board.

        If record_history is True, the previous board state is pushed onto the
        move history so the load can be undone with `undo_move()`. By default
        the move history is cleared (preserves previous behavior).
        """
        try:
            previous_board = self.board.copy()
            self.board.set_fen(fen)
            if record_history:
                # store a sentinel move None together with the previous board so undo_move works
                self.move_history.append((None, previous_board))
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
        return {
            "fen": self.get_fen(),
            "turn": "white" if self.board.turn else "black",
            "analysis": self.current_analysis,
            "legal_moves": self.get_legal_moves()
        }
