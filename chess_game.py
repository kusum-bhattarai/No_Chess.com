import chess
from collections import deque

class ChessGame:

    piece_symbols = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            '.': '·'
        }

    def __init__(self):
        self.board = chess.Board()
        
        #to store history for undo functionality
        self.move_history = deque()

    def display_board(self):

        print("  a b c d e f g h")
        print(" +-----------------+")
        for rank in range(7, -1, -1):
            print(f"{rank+1}| ", end="")
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                if piece:
                    print(self.piece_symbols[piece.symbol()], end=" ")
                else:
                    print(self.piece_symbols['.'], end=" ")
            print(f"|{rank+1}")
        print(" +-----------------+")
        print("  a b c d e f g h")

        turn = "White" if self.board.turn else "Black"
        print(f"\nCurrent turn: {turn}")
        if self.board.is_check():
            print("Check!")
        if self.board.is_checkmate():
            print("Checkmate!")
        if self.board.is_stalemate():
            print("Stalemate!")

    def make_move(self, move_str):
        try:
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.display_board()
                return True
            else:
                print(f"Illegal move: {move_str}")
                return False
        except ValueError:
            print(f"Invalid move format: {move_str}")
            return False

    def _add_to_history(self, move, previous_board):
        self.move_history.append((move, previous_board))

    def undo_move(self):
        if not self.move_history:
            print("No moves to undo.")
            return False
            
        #undo the last move and board state
        _, previous_board = self.move_history.pop()
        
        #restore the previous board state
        self.board = previous_board
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

