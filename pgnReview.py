import chess
import chess.pgn
import os
from utils import format_score, format_pv, get_evaluation_bar

class PgnReviewer:
    def __init__(self, engine):
        self.engine = engine
        self.board = chess.Board() # The board specifically for review purposes

    def clear_screen(self):
        os.system('clear')

    def display_board_for_review(self, analysis):
        """
        Displays the board state during review, including the evaluation bar.
        This is a simplified version of ChessGame's display_board tailored for review.
        """
        piece_symbols = {
            'r': '♜ ', 'n': '♞ ', 'b': '♝ ', 'q': '♛ ', 'k': '♚ ', 'p': '♟ ',
            'R': '♖ ', 'N': '♘ ', 'B': '♗ ', 'Q': '♕ ', 'K': '♔ ', 'P': '♙ ',
            '.': '· '
        }
        bar_height = 8 # Same as chess board height

        score = analysis.get("score", 0)
        is_mate = analysis.get("is_mate", False)

        eval_bar = get_evaluation_bar(score, is_mate, bar_height)
        score_text = format_score(score, is_mate)

        print("            a  b  c  d  e  f  g  h")
        print("          +------------------------+")
        for rank in range(7, -1, -1):
            bar_segment = eval_bar[7 - rank]
            if rank == 4:
                print(f"{bar_segment} {score_text} | {rank+1}|", end=" ")
            else:
                print(f"{bar_segment}      | {rank+1}|", end=" ")

            for file in range(8):
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    print(piece_symbols[piece.symbol()], end=" ")
                else:
                    print(piece_symbols['.'], end=" ")
            print(f"|{rank+1}")
        print("          +------------------------+")
        print("            a  b  c  d  e  f  g  h")

    def get_board_move_history_uci(self):
        """Helper to get move history for the review board."""
        return [move.uci() for move in self.board.move_stack]

    def perform_review(self, pgn_filepath):
        """
        Loads a PGN game, iterates through its moves, and provides Stockfish analysis
        for each move, similar to a game review.
        """
        try:
            with open(pgn_filepath) as pgn_file:
                game_node = chess.pgn.read_game(pgn_file)
                if game_node is None:
                    print(f"No valid chess game found in {pgn_filepath}.")
                    return

                # Reset the review board to the initial state
                self.board = chess.Board()

                # Display game metadata
                print(f"\n--- PGN Game Review: {game_node.headers.get('Event', 'Untitled Game')} ---")
                print(f"White: {game_node.headers.get('White', '?')} vs. Black: {game_node.headers.get('Black', '?')}")
                print(f"Result: {game_node.headers.get('Result', '*')}\n")

                move_counter = 1
                for move in game_node.mainline_moves():
                    self.clear_screen()

                    # Analyze position *before* the move
                    self.engine.set_position(self.get_board_move_history_uci())
                    pre_move_analysis = self.engine.analyze_position()

                    current_player_name = "White" if self.board.turn == chess.WHITE else "Black"

                    # Make the move on the review board
                    self.board.push(move)

                    # Analyze position *after* the move
                    self.engine.set_position(self.get_board_move_history_uci())
                    post_move_analysis = self.engine.analyze_position()

                    # Display the board and analysis
                    self.display_board_for_review(post_move_analysis) # Display board after the move, with its analysis

                    print(f"\n--- Move {move_counter}. {current_player_name} plays {move.uci()} ---")
                    print(f"Evaluation before move: {format_score(pre_move_analysis['score'], pre_move_analysis['is_mate'])}")
                    print(f"Stockfish's Best Move (pre-move): {pre_move_analysis['best_move']}")
                    print(f"Line (after Stockfish's best): {format_pv(pre_move_analysis['pv'][:4])}")
                    print(f"Evaluation after move: {format_score(post_move_analysis['score'], post_move_analysis['is_mate'])}")

                    # Basic comment generation logic
                    if pre_move_analysis['best_move'] and move.uci() != pre_move_analysis['best_move']:
                        score_diff = abs(pre_move_analysis['score'] if not pre_move_analysis['is_mate'] else 1000) - \
                                     abs(post_move_analysis['score'] if not post_move_analysis['is_mate'] else 1000)
                        if pre_move_analysis['is_mate'] and not post_move_analysis['is_mate']:
                            print("Comment: Missed a forced mate!")
                        elif score_diff > 200:
                            print("Comment: Blunder! A significant loss of advantage.")
                        elif score_diff > 50:
                            print("Comment: Mistake. There was a better move available.")
                        else:
                            print("Comment: Inaccuracy. Not the most precise, but still reasonable.")
                    else:
                        print("Comment: Excellent move! Matches Stockfish's top recommendation.")

                    input("Press Enter to continue to the next move review...")
                    move_counter += 1

                print("\n--- End of Game Review ---")
                # Show final state of the board in review
                self.clear_screen()
                self.display_board_for_review(post_move_analysis if 'post_move_analysis' in locals() else {"score": 0, "is_mate": False})
                print(f"Final game result: {game_node.headers.get('Result', '*')}")

        except FileNotFoundError:
            print(f"Error: PGN file not found at '{pgn_filepath}'.")
        except Exception as e:
            print(f"An error occurred during PGN parsing or review: {e}")