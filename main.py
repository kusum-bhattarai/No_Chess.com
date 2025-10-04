import argparse
import os
from engine import StockfishEngine
from chess_game import ChessGame
from pgnReview import PgnReviewer
from game_runner import GameRunner

def main():
    parser = argparse.ArgumentParser(description="NoChess.com - Terminal Chess Game")
    parser.add_argument("--mode", choices=["beginner", "intermediate", "advanced"], default="intermediate", help="Difficulty mode")
    parser.add_argument("--pgn", type=str, help="Path to PGN file for review (skips interactive if provided)")
    args = parser.parse_args()

    print("Welcome to NoChess.com!")
    print(f"Selected mode: {args.mode.capitalize()}")

    with StockfishEngine(args.mode) as engine:  # Auto-close engine
        if args.pgn and os.path.exists(args.pgn):
            print(f"Importing and analyzing {args.pgn}...")
            reviewer = PgnReviewer(engine)
            data = reviewer.perform_review(args.pgn)
            print("\nPGN game review complete.")
            print(f"Reviewed {len(data)} moves.")  # Example use of returned data
            play_new = input("Start interactive game? (y/n, default y): ").strip().lower()
            if play_new in ["n", "no"]:
                return
        else:
            if args.pgn:
                print(f"PGN file not found: {args.pgn}")

        game = ChessGame()
        runner = GameRunner(engine, game)
        runner.run()

if __name__ == "__main__":
    main()