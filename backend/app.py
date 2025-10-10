from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from .models import Mode, MoveRequest, StartGameRequest, AnalysisResponse, GameStateResponse, PgnReviewResponse
from .engine import StockfishEngine
from .chess_game import ChessGame
from typing import Dict
import asyncio
from fastapi import WebSocket, WebSocketDisconnect, File, UploadFile
from .pgnReview import PgnReviewer
import shutil
import chess.pgn
from fastapi.middleware.cors import CORSMiddleware

# Global in-memory sessions (dict: session_id -> ChessGame)
sessions: Dict[str, ChessGame] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Nothing yet
    yield
    # Shutdown: Close engines if needed
    pass

app = FastAPI(title="NoChess API", description="Terminal Chess to Web", version="0.1.0", lifespan=lifespan)
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

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
    
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        game = get_session(session_id)
        while True:
            # Get the latest analysis
            moves = game.get_move_history_uci()
            with StockfishEngine() as engine:
                engine.set_position(moves)
                analysis = engine.analyze_position()
                game.set_analysis(analysis)

            # Send the analysis to the client
            await websocket.send_json(analysis)

            # Wait for a short time before sending the next update
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        print(f"An error occurred in the websocket: {e}")
        await websocket.close(code=1011)

@app.post("/review_pgn", response_model=PgnReviewResponse)
def review_pgn(pgn_file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_path = f"/tmp/{pgn_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(pgn_file.file, buffer)

    try:
        with StockfishEngine() as engine:
            reviewer = PgnReviewer(engine)
            review_data = reviewer.perform_review(file_path)

            # Extract headers for the response
            with open(file_path) as pgn:
                game = chess.pgn.read_game(pgn)
                headers = game.headers if game else {}

        return {
            "review_data": review_data,
            "event": headers.get("Event", "Unknown Event"),
            "white": headers.get("White", "Unknown Player"),
            "black": headers.get("Black", "Unknown Player"),
            "result": headers.get("Result", "*"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to review PGN: {str(e)}")
    finally:
        # Clean up the temporary file
        import os
        if os.path.exists(file_path):
            os.remove(file_path)

# Add a simple health check endpoint for testing
@app.get("/")
def read_root():
    return {"message": "NoChess API is running"}