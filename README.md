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
- **Analyzes current position:** Analyzes current move and position and gives back user friendly analysis from StockFish's response.
- **Live Evaluation:** Evaluation bar showing position advantage along with the score.

## Prerequisites
Ensure you have Python installed on your system. Create a virtual environment and install the dependencies using:  
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

### Example Gameplay
```
            a  b  c  d  e  f  g  h
          +------------------------+
░      | 8| ♜  ♞  ♝  ♛  ♚  ♝  ♞  ♜  |8
░      | 7| ♟  ♟  ♟  ♟  ♟  ♟  ♟  ♟  |7
░      | 6| ·  ·  ·  ·  ·  ·  ·  ·  |6
░ 0.00 | 5| ·  ·  ·  ·  ·  ·  ·  ·  |5
█      | 4| ·  ·  ·  ·  ·  ·  ·  ·  |4
█      | 3| ·  ·  ·  ·  ·  ·  ·  ·  |3
█      | 2| ♙  ♙  ♙  ♙  ♙  ♙  ♙  ♙  |2
█      | 1| ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖  |1
          +------------------------+
            a  b  c  d  e  f  g  h

Current turn: White
Moves played: 0

Your move (or 'recommend', 'analyze', 'help'): 
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

### Recommend Command Output:
```
Your move (or 'recommend', 'analyze', 'help'): recommend
Stockfish recommends: b1c3
Make this move? (y/n):

```

### Analysis Command Output:
```
Stockfish Analysis:
Depth: 20
Evaluation: 0.28
Best move: d2d4
Line: d2d4 e5d4 d1d4 b8c6 d4d4 d4d4 d4d4 c6c6
Position: The position is roughly equal.

```

## Future Enhancements
- Add an evaluation bar on the left side similar to Chess.com.
- Integrate game review and analysis for an entire game.
- Add different modes for players to have fun with.
- Add GUI support for better visualization.
- Support PGN import/export for game tracking.
