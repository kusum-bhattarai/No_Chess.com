# backend/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from .models import Mode, MoveRequest, StartGameRequest, AnalysisResponse, GameStateResponse
from .engine import StockfishEngine
from .chess_game import ChessGame
from typing import Dict

# Global in-memory sessions (dict: session_id -> ChessGame)
sessions: Dict[str, ChessGame] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Nothing yet
    yield
    # Shutdown: Close engines if needed
    pass

app = FastAPI(title="NoChess API", description="Terminal Chess to Web", version="0.1.0", lifespan=lifespan)

# Dependency to get session (create if new)
def get_session(session_id: str) -> ChessGame:
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.post("/start_game", response_model=GameStateResponse)
def start_game(request: StartGameRequest):
    import uuid
    session_id = str(uuid.uuid4())
    try:
        with StockfishEngine(request.mode) as engine:
            game = ChessGame()
            # Initial analysis
            moves = game.get_move_history_uci()
            engine.set_position(moves)
            analysis = engine.analyze_position()
            game.set_analysis(analysis)
            sessions[session_id] = game
        
        state = game.get_state_json()
        state["session_id"] = session_id
        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")

@app.post("/make_move/{session_id}", response_model=GameStateResponse)
def make_move(session_id: str, request: MoveRequest, game: ChessGame = Depends(get_session)):
    try:
        if game.make_move(request.move):
            # Update analysis after player move
            moves = game.get_move_history_uci()
            with StockfishEngine() as engine:
                engine.set_position(moves)
                analysis = engine.analyze_position()
                game.set_analysis(analysis)
                
                # AI turn (simple: best move) - only if it's black's turn and game not over
                if not game.is_game_over() and not game.board.turn:  # Black's turn
                    best_move = analysis["best_move"]
                    if best_move and best_move != "(none)":
                        game.make_move(best_move)
                        # Update analysis again after AI move
                        moves = game.get_move_history_uci()
                        engine.set_position(moves)
                        analysis = engine.analyze_position()
                        game.set_analysis(analysis)
            
            state = game.get_state_json()
            state["session_id"] = session_id  # Add session_id to response
            return state
        else:
            raise HTTPException(status_code=400, detail="Invalid move")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Move failed: {str(e)}")

@app.get("/analyze/{session_id}", response_model=AnalysisResponse)
def analyze(session_id: str, game: ChessGame = Depends(get_session)):
    try:
        moves = game.get_move_history_uci()
        with StockfishEngine() as engine:
            engine.set_position(moves)
            analysis = engine.analyze_position()
        return AnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Add a simple health check endpoint for testing
@app.get("/")
def read_root():
    return {"message": "NoChess API is running"}