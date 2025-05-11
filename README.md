# No_Chess.com

## Overview
This is a simple terminal-based chess game implemented using the `python-chess` library. The game allows players to view the board, make legal moves, and check for conditions like check, checkmate, and stalemate. It is designed for fun and learning,capable of giving move recommendations and analysis(in future). Since chess.com only allows one free game review per day, this will help beginners analyze and mess with as many games as they want. (Beginners like me lol)

## Features
- **Display Board:** Prints the chessboard in the terminal with Unicode piece symbols.
- **Move Execution:** Allows users to enter moves in UCI (Universal Chess Interface) format.
- **Move Validation:** Checks for legality and invalid move formats.
- **Turn Tracking:** Indicates whose turn it is (White or Black).
- **Check and Checkmate Detection:** Notifies the player if a check, checkmate, or stalemate occurs.
- **Legal Moves Listing:** Displays all possible legal moves for the current position.
- **Recommends moves from StockFish Engine:** Displays the best move recommended by StockFish engine based on current board state.

## Prerequisites
Ensure you have Python installed on your system. You can install the dependencies using 
```
pip install -r requirements.txt
```

## How to Use
### Running the Game
1. Clone or download the script.
2. Open a terminal and navigate to the script's directory.
3. Run the script using:
   ```sh
   python main.py
   ```

### Available Commands
```
Available commands:
  e2e4, g1f3, etc.    - Make a move directly using UCI notation
  recommend           - Get Stockfish's recommended move
  analyze             - Analyze current position
  undo                - Undo the last move
  legal               - Show all legal moves
  fen                 - Show current position's FEN string
  load [fen]          - Load a position from a FEN string
  help                - Show this help message
  quit                - Exit the game
```

### Example Gameplay
```
 a  b  c  d  e  f  g  h
 +-----------------------+
8| ♜  ♞  ♝  ♛  ♚  ♝  ♞  ♜  |8
7| ♟  ♟  ♟  ♟  ♟  ♟  ♟  ♟  |7
6| ·  ·  ·  ·  ·  ·  ·  ·  |6
5| ·  ·  ·  ·  ·  ·  ·  ·  |5
4| ·  ·  ·  ·  ♙  ·  ·  ·  |4
3| ·  ·  ·  ·  ·  ·  ·  ·  |3
2| ♙  ♙  ♙  ♙  ·  ♙  ♙  ♙  |2
1| ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖  |1
 +-----------------------+
   a  b  c  d  e  f  g  h

Current turn: Black
Moves played: 1

Your move (or 'recommend', 'analyze', 'help'): 
```

## Known Issues
- The program only gives recommendations on best move for now but lacks the implementation for analysis or evaluation.

## Future Enhancements
- Add GUI support for better visualization.
- Support PGN import/export for game tracking.
