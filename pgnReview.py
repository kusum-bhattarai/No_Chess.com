import chess
import chess.pgn
import os
from typing import List, Dict
from utils import format_score, format_pv
from ui.terminal_ui import TerminalUI

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
        """Generate comment based on analysis difference."""
        if not pre_analysis.get('best_move') or move_uci == pre_analysis['best_move']:
            return "Comment: Excellent move! Matches Stockfish's top recommendation."

        # Calculate score diff (absolute, mate as 1000+)
        pre_score = abs(pre_analysis['score']) if not pre_analysis['is_mate'] else 1000
        post_score = abs(post_analysis['score']) if not post_analysis['is_mate'] else 1000
        score_diff = pre_score - post_score  # Positive if loss

        if post_score > pre_score + 50:
            return "Comment: Brilliant! Better than Stockfish's recommendation."
        elif pre_analysis['is_mate'] and not post_analysis['is_mate']:
            return "Comment: Missed a forced mate!"
        elif score_diff > 200:
            return "Comment: Blunder! A significant loss of advantage."
        elif score_diff > 50:
            return "Comment: Mistake. There was a better move available."
        else:
            return "Comment: Inaccuracy. Not the most precise, but still reasonable."

    def perform_review(self, pgn_filepath: str, quick_mode: bool = False, pause: bool = False) -> List[Dict]:
        """
        Loads a PGN game, iterates through its moves, and provides Stockfish analysis
        for each move, similar to a game review. Returns structured review data.

        Args:
            pgn_filepath: Path to PGN file.
            quick_mode: If True, use reduced depth for faster review.

        Returns:
            List of dicts with review data per move.
        """
        if quick_mode:
            self.review_depth = 10
        else:
            self.review_depth = 20

        review_data = []
        try:
            with open(pgn_filepath) as pgn_file:
                game_node = chess.pgn.read_game(pgn_file)
                if game_node is None:
                    print(f"No valid chess game found in {pgn_filepath}.")
                    return review_data

                # Reset the review board to the initial state
                self.board = chess.Board()

                # Collect moves into a list so we can validate the game has moves and
                # avoid consuming a generator multiple times.
                moves = list(game_node.mainline_moves())
                if not moves:
                    print(f"No valid chess game found in {pgn_filepath}.")
                    return review_data

                # Display game metadata
                print(f"\n--- PGN Game Review: {game_node.headers.get('Event', 'Untitled Game')} ---")
                print(f"White: {game_node.headers.get('White', '?')} vs. Black: {game_node.headers.get('Black', '?')}")
                print(f"Result: {game_node.headers.get('Result', '*')}\n")

                move_counter = 1
                for move in moves:
                    self.clear_screen()  # Still need this? UI has it, but call if needed

                    # Analyze position *before* the move
                    self.engine.set_position(self.get_board_move_history_uci())
                    pre_move_analysis = self.engine.analyze_position(depth=self.review_depth)

                    current_player_name = "White" if self.board.turn == chess.WHITE else "Black"

                    # Make the move on the review board
                    self.board.push(move)

                    # Analyze position *after* the move
                    self.engine.set_position(self.get_board_move_history_uci())
                    post_move_analysis = self.engine.analyze_position(depth=self.review_depth)

                    # Display the board and analysis
                    self.display_board_for_review(post_move_analysis)  # Display after move

                    print(f"\n--- Move {move_counter}. {current_player_name} plays {move.uci()} ---")
                    print(f"Evaluation before move: {format_score(pre_move_analysis['score'], pre_move_analysis['is_mate'])}")
                    print(f"Stockfish's Best Move (pre-move): {pre_move_analysis['best_move']}")
                    print(f"Line (after Stockfish's best): {format_pv(pre_move_analysis['pv'][:4])}")
                    print(f"Evaluation after move: {format_score(post_move_analysis['score'], post_move_analysis['is_mate'])}")

                    # Generate and print comment
                    comment = self._generate_comment(pre_move_analysis, post_move_analysis, move.uci())
                    print(comment)

                    # Add to review data
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
                        input("Press Enter to continue to the next move review...")
                    move_counter += 1

                print("\n--- End of Game Review ---")
                # Show final state of the board in review
                default_analysis = {"score": 0, "is_mate": False, "best_move": None, "pv": [], "depth": 0}
                final_analysis = post_move_analysis if 'post_move_analysis' in locals() else default_analysis
                self.clear_screen()
                self.display_board_for_review(final_analysis)
                print(f"Final game result: {game_node.headers.get('Result', '*')}")

                return review_data

        except FileNotFoundError:
            print(f"Error: PGN file not found at '{pgn_filepath}'.")
        except Exception as e:
            # catch broad exceptions related to parsing/IO and report them.
            print(f"PGN parsing error: {e}")
        except Exception as e:
            print(f"An error occurred during PGN parsing or review: {e}")
        return review_data

    def clear_screen(self):
        """Clear screen for review display."""
        os.system('clear')