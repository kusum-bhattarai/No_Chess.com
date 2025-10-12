from pydantic import BaseModel
from typing import List, Dict, Optional, Literal
from enum import Enum

class Mode(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class MoveRequest(BaseModel):
    move: str  # e.g., "e2e4"

class StartGameRequest(BaseModel):
    mode: Optional[Mode] = "intermediate"

class AnalysisResponse(BaseModel):
    score: float
    is_mate: bool
    best_move: Optional[str] = None
    pv: List[str] = []
    depth: Optional[int] = None

class GameStateResponse(BaseModel):
    session_id: str
    fen: str
    turn: Literal["white", "black"]
    legal_moves: List[str]
    analysis: Optional[AnalysisResponse] = None
    game_over: bool
    result: Optional[str] = None       # "1-0" | "0-1" | "1/2-1/2"
    status: Optional[str] = None       # "Checkmate", "Stalemate", etc.
    user_color: Literal["white", "black"]
    in_check: bool = False
    in_checkmate: bool = False
    in_stalemate: bool = False
    is_draw: bool = False
    draw_reason: Optional[str] = None
    last_move: Optional[str] = None

class ReviewMove(BaseModel):
    move_number: int
    move: str
    player: str
    pre_eval: Dict
    post_eval: Dict
    best_move: Optional[str] = None
    pv: str
    comment: str

class PgnReviewResponse(BaseModel):
    review_data: List[ReviewMove]
    event: str
    white: str
    black: str
    result: str