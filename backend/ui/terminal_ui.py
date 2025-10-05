import os
import chess
from typing import Dict
from ..utils import format_score, get_evaluation_bar, get_piece_symbols, format_pv

class TerminalUI:
    def __init__(self, max_score: int = 500):
        self.max_score = max_score

    def clear_screen(self):
        os.system('clear')

    def display_board(self, board, analysis: Dict, clear: bool = True):
        if clear:
            self.clear_screen()
        bar_height = 8
        score = analysis["score"]
        is_mate = analysis["is_mate"]
        streak = self._calculate_streak(score, is_mate, bar_height)
        eval_bar = get_evaluation_bar(streak, is_mate, bar_height)
        score_text = format_score(score, is_mate)
        piece_symbols = get_piece_symbols()

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
                piece = board.piece_at(square)
                if piece:
                    print(piece_symbols[piece.symbol()], end=" ")
                else:
                    print(piece_symbols['.'], end=" ")
            print(f"|{rank+1}")
        print("          +------------------------+")
        print("            a  b  c  d  e  f  g  h")
        self.display_game_state(board)

    def _calculate_streak(self, score: int, is_mate: bool, height: int) -> int:
        if is_mate:
            return height if score > 0 else 0
        capped_score = max(min(score, self.max_score), -self.max_score)
        return int((capped_score + self.max_score) * height / (2 * self.max_score))

    def display_game_state(self, board):
        turn = "White" if board.turn else "Black"
        print(f"\nCurrent turn: {turn}")
        if board.is_checkmate():
            print("Checkmate! Game over.")
        elif board.is_stalemate():
            print("Stalemate! Game over.")
        elif board.is_insufficient_material():
            print("Insufficient material! Game over.")
        elif board.is_check():
            print("Check!")
        print(f"Moves played: {len(board.move_stack)}")  # Use board.move_stack for count

    def display_analysis(self, board, analysis: Dict):
        score = analysis["score"]
        is_mate = analysis["is_mate"]
        best_move = analysis["best_move"]
        pv = analysis["pv"]
        depth = analysis["depth"]
        score_str = format_score(score, is_mate)
        pv_str = format_pv(pv[:4])

        if is_mate:
            insight = f"{'White' if score > 0 else 'Black'} can deliver checkmate in {abs(score)} move(s)."
        else:
            if abs(score) < 50:
                insight = "The position is roughly equal."
            elif score > 0:
                insight = f"White has a {'slight' if score < 200 else 'strong'} advantage."
            else:
                insight = f"Black has a {'slight' if score > -200 else 'strong'} advantage."

        self.display_board(board, analysis, clear=True)
        print("\nStockfish Analysis:")
        print(f"Depth: {depth}")
        print(f"Evaluation: {score_str}")
        print(f"Best move: {best_move[:2]}{best_move[2:]}")
        print(f"Line: {pv_str}")
        print(f"Position: {insight}")