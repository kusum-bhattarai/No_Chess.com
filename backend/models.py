from pydantic import BaseModel
from typing import List, Dict, Optional
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
    pv: List[str]
    depth: int

class GameStateResponse(BaseModel):
    session_id: str
    fen: str
    turn: str
    legal_moves: List[str]
    analysis: Dict
    game_over: bool
    result: Optional[str] = None

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