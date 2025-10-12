from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, File, UploadFile
from typing import Dict, Union
import uuid
import asyncio
import shutil
import chess
import chess.pgn
import os
import traceback 
import random

from .pgnReview import PgnReviewer
from .models import Mode, MoveRequest, StartGameRequest, AnalysisResponse, GameStateResponse, PgnReviewResponse
from .engine import StockfishEngine
from .chess_game import ChessGame
from fastapi.middleware.cors import CORSMiddleware

sessions: Dict[str, Dict[str, Union[ChessGame, StockfishEngine, str]]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Shutting down and closing all Stockfish engines...")
    for session_id, session_data in sessions.items():
        engine = session_data.get("engine")
        if engine:
            print(f"Closing engine for session {session_id}")
            engine.close()

app = FastAPI(title="NoChess API", description="Terminal Chess to Web", version="0.1.0", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session_data(session_id: str) -> Dict:
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

def get_game(session_data: Dict = Depends(get_session_data)) -> ChessGame:
    return session_data["game"]

def get_engine(session_data: Dict = Depends(get_session_data)) -> StockfishEngine:
    return session_data["engine"]

@app.post("/start_game", response_model=GameStateResponse)
def start_game(request: StartGameRequest):
    session_id = str(uuid.uuid4())
    try:
        mode_str = request.mode.value if request.mode else "intermediate"
        print(f"Attempting to start Stockfish with mode: {mode_str}")

        engine = StockfishEngine(mode=mode_str)
        game = ChessGame()
        print("Stockfish engine initialized successfully.")

        moves = game.get_move_history_uci()
        engine.set_position(moves)
        analysis = engine.analyze_position()
        game.set_analysis(analysis)

        # Randomly assign user color; if user is black, AI (white) moves first
        user_color = random.choice(["white", "black"])
        if user_color == "black":
            best_move = analysis.get("best_move")
            if best_move and best_move != "(none)":
                game.make_move(best_move)
                moves = game.get_move_history_uci()
                engine.set_position(moves)
                analysis = engine.analyze_position()
                game.set_analysis(analysis)

        sessions[session_id] = {"game": game, "engine": engine, "user_color": user_color}
        print(f"New session created: {session_id}")

        state = game.get_state_json()
        state["session_id"] = session_id
        state["user_color"] = user_color
        return state
    except Exception as e:
        print("\n--- ERROR IN /start_game ---")
        traceback.print_exc()
        print("--------------------------\n")
        raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")

@app.post("/make_move/{session_id}", response_model=GameStateResponse)
def make_move(session_id: str, request: MoveRequest, game: ChessGame = Depends(get_game), engine: StockfishEngine = Depends(get_engine)):
    try:
        if game.make_move(request.move):
            moves = game.get_move_history_uci()
            engine.set_position(moves)
            analysis = engine.analyze_position()
            game.set_analysis(analysis)

            if not game.is_game_over() and game.board.turn == chess.BLACK:
                best_move = analysis.get("best_move")
                if best_move and best_move != "(none)":
                    game.make_move(best_move)
                    moves = game.get_move_history_uci()
                    engine.set_position(moves)
                    analysis = engine.analyze_position()
                    game.set_analysis(analysis)

            state = game.get_state_json()
            state["session_id"] = session_id
            session_data = sessions.get(session_id, {})
            state["user_color"] = session_data.get("user_color")
            return state
        else:
            raise HTTPException(status_code=400, detail="Invalid move")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Move failed: {str(e)}")

@app.get("/analyze/{session_id}", response_model=AnalysisResponse)
def analyze(session_id: str, game: ChessGame = Depends(get_game), engine: StockfishEngine = Depends(get_engine)):
    try:
        moves = game.get_move_history_uci()
        engine.set_position(moves)
        analysis = engine.analyze_position()
        return AnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        session_data = get_session_data(session_id)
        game = session_data["game"]
        engine = session_data["engine"]
        while True:
            moves = game.get_move_history_uci()
            engine.set_position(moves)
            analysis = engine.analyze_position()
            game.set_analysis(analysis)
            await websocket.send_json(analysis)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        # Avoid explicit close to prevent incompatibility issues between uvicorn/starlette/websockets
        print(f"An error occurred in the websocket for session {session_id}: {e}")
        return

@app.post("/review_pgn", response_model=PgnReviewResponse)
def review_pgn(pgn_file: UploadFile = File(...), quick_mode: bool = False):
    file_path = f"/tmp/{pgn_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(pgn_file.file, buffer)
    try:
        with StockfishEngine() as engine:
            reviewer = PgnReviewer(engine)
            review_data = reviewer.perform_review(file_path, quick_mode=quick_mode)
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
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/")
def read_root():
    return {"message": "NoChess API is running"}

@app.post("/resign/{session_id}", response_model=GameStateResponse)
def resign(session_id: str):
    session_data = get_session_data(session_id)
    game: ChessGame = session_data["game"]
    user_color: str = session_data.get("user_color", "white")
    game.resign(user_color)
    state = game.get_state_json()
    state["session_id"] = session_id
    state["user_color"] = user_color
    return state

@app.post("/restart/{session_id}", response_model=GameStateResponse)
def restart(session_id: str):
    session_data = get_session_data(session_id)
    game: ChessGame = session_data["game"]
    engine: StockfishEngine = session_data["engine"]

    game.restart()
    engine.set_position([])
    analysis = engine.analyze_position()
    game.set_analysis(analysis)

    # Randomly reassign user color; if user is black, let AI (white) move first
    user_color = random.choice(["white", "black"])
    if user_color == "black":
        best_move = analysis.get("best_move")
        if best_move and best_move != "(none)":
            game.make_move(best_move)
            moves = game.get_move_history_uci()
            engine.set_position(moves)
            analysis = engine.analyze_position()
            game.set_analysis(analysis)

    session_data["user_color"] = user_color
    state = game.get_state_json()
    state["session_id"] = session_id
    state["user_color"] = user_color
    return state
