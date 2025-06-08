import chess
from chess_game import ChessGame
from engine import StockfishEngine
from pgnReview import PgnReviewer
import os

def clear_screen():
    os.system('clear')



def print_help():
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

def main():
    clear_screen()
    print("Welcome to NoChess.com!")
    print("Choose a difficulty mode:")
    print("1. Beginner")
    print("2. Intermediate")
    print("3. Advanced")
    
    mode_choice = input("Select mode (1-3, default is Intermediate): ").strip()
    
    #mapping user input to modes
    mode_map = {
        "1": "beginner",
        "2": "intermediate", 
        "3": "advanced"
    }
    
    #default mode in case of invalid input
    mode = mode_map.get(mode_choice, "intermediate")
    print(f"Selected mode: {mode.capitalize()}")
    
    #initialize the engine
    engine = StockfishEngine(mode)
    
    #initialize the game class
    game = ChessGame()

    # PGN Import 
    import_pgn_choice = input("\nDo you want to import a PGN game for review? (y/n, default n): ").strip().lower()
    if import_pgn_choice == "y" or import_pgn_choice == "yes":
        pgn_filepath = input("Enter the path to your PGN file: ").strip()
        if os.path.exists(pgn_filepath):
            print(f"Importing and analyzing {pgn_filepath}...")
            pgn_reviewer = PgnReviewer(engine) # Instantiate the new PgnReviewer class
            pgn_reviewer.perform_review(pgn_filepath) # Call its review method
            print("\nPGN game review complete. You can now choose to start a new game or exit.")
            play_new_game_after_review = input("Start a new game? (y/n, default y): ").strip().lower()
            if play_new_game_after_review == "n" or play_new_game_after_review == "no":
                print("Thank you for using NoChess.com!")
                return
            else:
                game = ChessGame() # Re-initialize for a new interactive game
        else:
            print(f"Error: PGN file not found at {pgn_filepath}. Starting a regular game instead.")
    
    #display the board
    game.display_board()
    
    # Print help at the start
    print_help()
    
    while not game.is_game_over():
        #get user input and process commands
        user_input = input("\nYour move (or 'recommend', 'analyze', 'help'): ").strip().lower()
        
        if user_input == "quit" or user_input == "exit":
            print("Thanks for playing!")
            break
            
        elif user_input == "help":
            print_help()
            #redisplay the saved board state after help
            
        elif user_input == "recommend":
            #get move history in UCI format
            moves = game.get_move_history_uci()
            
            #set the position in the engine
            engine.set_position(moves)
            
            #get and display the recommended move
            best_move = engine.get_best_move()
            print(f"Stockfish recommends: {best_move}")
            
            #show what this move would look like on the board
            confirm = input("Make this move? (y/n): ").strip().lower()
            if confirm == "y" or confirm == "yes":
                success = game.make_move(best_move)
                #update analysis after making the recommended move
                if success:
                    moves = game.get_move_history_uci()
                    engine.set_position(moves)
                    analysis = engine.analyze_position()
                    game.set_analysis(analysis)
            else:
                #redisplay the board if the user doesn't take the recommendation
                game.display_board()
                
        elif user_input == "analyze":
            # Get move history in UCI format
            moves = game.get_move_history_uci()
            
            # Set the position in the engine
            engine.set_position(moves)
            
            # Get analysis
            analysis = engine.analyze_position()
            
            # Display analysis
            game.display_analysis(analysis)
            
            # Prompt to return to game
            input("Press Enter to continue...")
            game.display_board()
            
        elif user_input == "undo":
            #update analysis after undoing 
            if game.undo_move():
                moves = game.get_move_history_uci()
                engine.set_position(moves)
                analysis = engine.analyze_position()
                game.set_analysis(analysis)

            
        elif user_input == "legal":
            game.print_legal_moves()
            # After showing legal moves, redisplay the board
            input("Press Enter to continue...")
            game.display_board()
            
        elif user_input == "fen":
            print(f"Current FEN: {game.get_fen()}")
            
        elif user_input.startswith("load "):
            #extract the FEN string from the command
            fen = user_input[5:].strip()
            game.load_fen(fen)
            
        #default input would be moves
        else:
            success = game.make_move(user_input)

            #for analysis at every move
            if success:
                #get move history in uci format
                moves = game.get_move_history_uci()
            
                #set the position in the engine
                engine.set_position(moves)
            
                #get analysis
                analysis = engine.analyze_position()
            
                #update the game with analysis
                game.set_analysis(analysis)

            else:
                print("Invalid move. Type 'legal' to see valid moves or 'help' for commands.")
                input("Press Enter to continue...")
            game.display_board()
    
    result = game.get_game_result()
    print("\nGame over!")
    print(result)
    
    #ask if user wants to play again
    play_again = input("\nPlay again? (y/n): ").strip().lower()
    if play_again == "y" or play_again == "yes":
        main()  #restart the game
    else:
        print("Thank you for playing NoChess.com!")

if __name__ == "__main__":
    main()
