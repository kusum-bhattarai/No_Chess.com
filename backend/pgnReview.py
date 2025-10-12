import chess
import chess.pgn
import os
from typing import List, Dict
from .utils import format_score, format_pv
from .ui.terminal_ui import TerminalUI

class PgnReviewer:
    def __init__(self, engine, quick_mode: bool = False, review_depth: int = 20):
        self.engine = engine
        self.board = chess.Board()  # The board specifically for review purposes
        self.ui = TerminalUI()  # Reuse shared UI for display
        self.quick_mode = quick_mode
        self.review_depth = 10 if quick_mode else review_depth

    def display_board_for_review(self, analysis: Dict):
        """
        Displays the board state during review, including the evaluation bar.
        Delegates to TerminalUI for consistency.
        """
        self.ui.display_board(self.board, analysis, clear=True)

    def get_board_move_history_uci(self):
        """Helper to get move history for the review board."""
        return [move.uci() for move in self.board.move_stack]

    def _generate_comment(self, pre_analysis: Dict, post_analysis: Dict, move_uci: str) -> str:
        """Generate comment with standard keywords."""
        pre_best = pre_analysis.get('best_move')
        pre_is_mate = pre_analysis.get('is_mate')
        post_is_mate = post_analysis.get('is_mate')
        pre_score = abs(pre_analysis['score']) if not pre_is_mate else 1000
        post_score = abs(post_analysis['score']) if not post_is_mate else 1000
        score_diff = pre_score - post_score  # positive => loss

        if not pre_best or move_uci == pre_best:
            return "Best: Matches engine recommendation."
        
        if pre_is_mate and not post_is_mate:
            return "Blunder: Missed a forced mate."
        if post_score > pre_score + 100:
            return "Brilliant: Improved beyond engine line."
        if score_diff > 300:
            return "Blunder: Major loss of advantage."
        if score_diff > 100:
            return "Mistake: Clear better move existed."
        if score_diff > 30:
            return "Inaccuracy: Slightly suboptimal."
        return "Great: Solid move."
    
    def _read_first_valid_game(self, pgn_filepath: str):
        try:
            with open(pgn_filepath) as f:
                while True:
                    game_node = chess.pgn.read_game(f)
                    if game_node is None:
                        return None, []
                    moves = list(game_node.mainline_moves())
                    if moves:
                        return game_node, moves
        except Exception:
            return None, []

    def perform_review(self, pgn_filepath: str, quick_mode: bool = False, pause: bool = False) -> List[Dict]:
        self.review_depth = 10 if quick_mode else 20
        review_data = []
        try:
            game_node, moves = self._read_first_valid_game(pgn_filepath)
            if game_node is None or not moves:
                print(f"No valid chess game with moves found in {pgn_filepath}.")
                return review_data

            self.board = chess.Board()
            move_counter = 1
            for move in moves:
                self.clear_screen()

                self.engine.set_position(self.get_board_move_history_uci())
                self.engine.set_depth(self.review_depth)
                pre_move_analysis = self.engine.analyze_position()

                current_player_name = "White" if self.board.turn == chess.WHITE else "Black"
                self.board.push(move)

                self.engine.set_position(self.get_board_move_history_uci())
                self.engine.set_depth(self.review_depth)
                post_move_analysis = self.engine.analyze_position()

                self.display_board_for_review(post_move_analysis)

                from .utils import format_score, format_pv
                comment = self._generate_comment(pre_move_analysis, post_move_analysis, move.uci())

                review_data.append({
                    "move_number": move_counter,
                    "move": move.uci(),
                    "player": current_player_name,
                    "pre_eval": {
                        "score": pre_move_analysis['score'],
                        "is_mate": pre_move_analysis['is_mate'],
                        "formatted": format_score(pre_move_analysis['score'], pre_move_analysis['is_mate'])
                    },
                    "post_eval": {
                        "score": post_move_analysis['score'],
                        "is_mate": post_move_analysis['is_mate'],
                        "formatted": format_score(post_move_analysis['score'], post_move_analysis['is_mate'])
                    },
                    "best_move": pre_move_analysis['best_move'],
                    "pv": format_pv(pre_move_analysis['pv'][:4]),
                    "comment": comment
                })

                if pause:
                    input("Press Enter to continue...")
                move_counter += 1

            print("\n--- End of Game Review ---")
            default_analysis = {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0}
            final_analysis = post_move_analysis if 'post_move_analysis' in locals() else default_analysis
            self.clear_screen()
            self.display_board_for_review(final_analysis)
            print(f"Final game result: {game_node.headers.get('Result', '*')}")

            return review_data

        except FileNotFoundError:
            print(f"Error: PGN file not found at '{pgn_filepath}'.")
        except Exception as e:
            print(f"PGN parsing error: {e}")
        return review_data

    def clear_screen(self):
        """Clear screen for review display."""
        os.system('clear')