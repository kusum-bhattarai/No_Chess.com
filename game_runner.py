import argparse
from typing import Optional
from chess_game import ChessGame
from engine import StockfishEngine

class GameRunner:
    def __init__(self, engine: StockfishEngine, game: ChessGame):
        self.engine = engine
        self.game = game
        self.running = True

    def print_help(self):
        print("\nAvailable commands:")
        print("  e2e4, g1f3, etc.    - Make a move directly using UCI notation")
        print("  recommend           - Get Stockfish's recommended move")
        print("  analyze             - Analyze current position")
        print("  undo                - Undo the last move")
        print("  legal               - Show all legal moves")
        print("  fen                 - Show current position's FEN string")
        print("  load [fen]          - Load a position from a FEN string")
        print("  help                - Show this help message")
        print("  quit                - Exit the game")

    def process_command(self, user_input: str) -> bool:
        """Process a single command; return False to quit."""
        user_input = user_input.strip().lower()

        if user_input in ["quit", "exit"]:
            print("Thanks for playing!")
            return False

        elif user_input == "help":
            self.print_help()
            self.game.display_board()  # Redisplay after help
            return True

        elif user_input == "recommend":
            moves = self.game.get_move_history_uci()
            self.engine.set_position(moves)
            best_move = self.engine.get_best_move()
            print(f"Stockfish recommends: {best_move}")
            confirm = input("Make this move? (y/n): ").strip().lower()
            if confirm in ["y", "yes"]:
                success = self.game.make_move(best_move)
                if success:
                    moves = self.game.get_move_history_uci()
                    self.engine.set_position(moves)
                    analysis = self.engine.analyze_position()
                    self.game.set_analysis(analysis)
            else:
                self.game.display_board()
            return True

        elif user_input == "analyze":
            moves = self.game.get_move_history_uci()
            self.engine.set_position(moves)
            analysis = self.engine.analyze_position()
            self.game.display_analysis(analysis)
            input("Press Enter to continue...")
            self.game.display_board()
            return True

        elif user_input == "undo":
            if self.game.undo_move():
                moves = self.game.get_move_history_uci()
                self.engine.set_position(moves)
                analysis = self.engine.analyze_position()
                self.game.set_analysis(analysis)
            return True

        elif user_input == "legal":
            self.game.print_legal_moves()
            input("Press Enter to continue...")
            self.game.display_board()
            return True

        elif user_input == "fen":
            print(f"Current FEN: {self.game.get_fen()}")
            return True

        elif user_input.startswith("load "):
            fen = user_input[5:].strip()
            self.game.load_fen(fen)
            return True

        else:  # Assume move
            success = self.game.make_move(user_input)
            if success:
                moves = self.game.get_move_history_uci()
                self.engine.set_position(moves)
                analysis = self.engine.analyze_position()
                self.game.set_analysis(analysis)
            else:
                print("Invalid move. Type 'legal' to see valid moves or 'help' for commands.")
                input("Press Enter to continue...")
            self.game.display_board()
            return True

    def run(self) -> bool:
        """Run the interactive game loop; return True if played again."""
        self.game.display_board()
        self.print_help()

        while not self.game.is_game_over() and self.running:
            user_input = input("\nYour move (or 'recommend', 'analyze', 'help'): ")
            self.running = self.process_command(user_input)

        if self.game.is_game_over():
            result = self.game.get_game_result()
            print("\nGame over!")
            print(result)

        # Non-recursive play again
        while True:
            play_again = input("\nPlay again? (y/n): ").strip().lower()
            if play_again in ["y", "yes"]:
                self.game = ChessGame()  # Reset game
                return self.run()  # Recursive here is fine (depth-limited), or loop externally
            elif play_again in ["n", "no"]:
                print("Thank you for playing NoChess.com!")
                return False
            else:
                print("Please enter y or n.")

# Argparse integration (to be called from main.py)
def create_parser():
    parser = argparse.ArgumentParser(description="NoChess.com CLI")
    parser.add_argument("--mode", choices=["beginner", "intermediate", "advanced"], default="intermediate", help="Difficulty mode")
    parser.add_argument("--pgn", type=str, help="Path to PGN file for review")
    return parser