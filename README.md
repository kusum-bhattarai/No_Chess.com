# No_Chess.com

## Overview
This is a simple terminal-based chess game implemented using the `python-chess` library. The game allows players to view the board, make legal moves, and check for conditions like check, checkmate, and stalemate. It is designed for fun and learning, with the potential to evolve into a more advanced chess engine with move recommendations and analysis. Since chess.com only allows one free game review per day, this will help beginners analyze and mess with as many games as they want. (Beginners like me lol)

## Features
- **Display Board:** Prints the chessboard in the terminal with Unicode piece symbols.
- **Move Execution:** Allows users to enter moves in UCI (Universal Chess Interface) format.
- **Move Validation:** Checks for legality and invalid move formats.
- **Turn Tracking:** Indicates whose turn it is (White or Black).
- **Check and Checkmate Detection:** Notifies the player if a check, checkmate, or stalemate occurs.
- **Legal Moves Listing:** Displays all possible legal moves for the current position.

## Prerequisites
Ensure you have Python installed on your system. You also need the `python-chess` library, which can be installed using:

```sh
pip install python-chess
```

## How to Use
### Running the Game
1. Clone or download the script.
2. Open a terminal and navigate to the script's directory.
3. Run the script using:
   ```sh
   python chess.py
   ```

### Available Commands
- **Display the Board:** The board is displayed at the start and after each valid move.
- **Make a Move (make_move):** Enter moves using the UCI notation (e.g., `e2e4` to move a piece from e2 to e4).
- **Print Legal Moves (print_legal_moves):** The script provides a list of legal moves, grouped by piece position.

### Example Gameplay
```
  a b c d e f g h
 +-----------------+
8| ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ |8
7| ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ |7
6| · · · · · · · · |6
5| · · · · · · · · |5
4| · · · · · · · · |4
3| · · · · · · · · |3
2| ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ |2
1| ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ |1
 +-----------------+
  a b c d e f g h

Current turn: White

> Move: e2e4
> Move: d7d5
> Move: g1f3
```

## Known Issues
- The script currently does not support castling, en passant, or promotion handling.
- The input system is limited to UCI notation without interactive guidance.

## Future Enhancements
- Implement an AI-based move recommender and analyzer using Stockfish engine.
- Add GUI support for better visualization.
- Support PGN import/export for game tracking.
