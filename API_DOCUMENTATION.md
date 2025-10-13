# NoChess API Documentation

Version: 0.1.0  
Base URL (local): `http://localhost:8000`

- Authentication: None (local dev)
- Content types: `application/json` unless noted
- CORS: Allowed for `http://localhost:5173` and `http://127.0.0.1:5173`

## Conventions

- All responses are JSON.
- Errors return appropriate HTTP status with a `detail` message.
- Sessions: Each game session is identified by `session_id` returned from `/start_game`.

## Models

### Enum: Mode
- beginner
- intermediate
- advanced
Note: Currently accepted by `StartGameRequest` for parity; engine setup does not require it.

### StartGameRequest
```json
{
  "mode": "intermediate"
}
```
- mode: optional enum (default: "intermediate")

### MoveRequest
```json
{
  "move": "e2e4"
}
```
- move: required UCI move string

### AnalysisResponse
```json
{
  "score": 23,
  "is_mate": false,
  "best_move": "e2e4",
  "pv": ["e2e4","e7e5","g1f3","b8c6"],
  "depth": 12
}
```
- score: centipawns (relative to side to move); if `is_mate` true, value is mate distance sign.
- is_mate: boolean
- best_move: best move in UCI (if available)
- pv: principal variation in UCI
- depth: engine search depth

### GameStateResponse
```json
{
  "session_id": "uuid",
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "turn": "white",
  "legal_moves": ["e2e4","d2d4","g1f3", "..."],
  "analysis": {
    "score": 23,
    "is_mate": false,
    "best_move": "e2e4",
    "pv": ["e2e4","e7e5","g1f3","b8c6"],
    "depth": 12
  },
  "game_over": false,
  "result": null,
  "status": "In progress",
  "user_color": "white",
  "in_check": false,
  "in_checkmate": false,
  "in_stalemate": false,
  "is_draw": false,
  "draw_reason": null,
  "last_move": null
}
```
- session_id: the current game session
- fen: position
- turn: "white" or "black"
- legal_moves: list of UCI moves
- analysis: optional AnalysisResponse
- game_over: bool
- result: "1-0" | "0-1" | "1/2-1/2" | null
- status: human-readable status
- user_color: "white" | "black"
- in_check, in_checkmate, in_stalemate, is_draw, draw_reason: flags and info
- last_move: last applied UCI, if any

### ReviewMove
```json
{
  "move_number": 1,
  "move": "e2e4",
  "player": "White",
  "pre_eval": { "score": 20, "is_mate": false, "formatted": "+0.20" },
  "post_eval": { "score": 35, "is_mate": false, "formatted": "+0.35" },
  "best_move": "e2e4",
  "pv": "e2e4 e7e5 g1f3 b8c6",
  "comment": "Best: Matches engine recommendation."
}
```

### PgnReviewResponse
```json
{
  "review_data": [ /* array of ReviewMove */ ],
  "event": "My Tournament",
  "white": "Alice",
  "black": "Bob",
  "result": "1-0"
}
```

## Endpoints

### GET `/`
Health check
- 200: `{ "message": "NoChess API is running" }`

### POST `/start_game`
Start a new session (randomizes user color).
- Body: StartGameRequest (optional `mode`)
- 200: GameStateResponse
- 500: Failed to start game

Example:
```bash
curl -X POST http://localhost:8000/start_game \
  -H "Content-Type: application/json" \
  -d '{"mode":"intermediate"}'
```

### POST `/make_move/{session_id}`
Apply a user UCI move; the engine will reply if it is its turn.
- Path: `session_id` (string)
- Body: MoveRequest
- 200: GameStateResponse (always returns state; illegal move sets `status` accordingly)
- 404: Unknown session

Example:
```bash
curl -X POST http://localhost:8000/make_move/SESSION_ID \
  -H "Content-Type: application/json" \
  -d '{"move":"e2e4"}'
```

### GET `/analyze/{session_id}`
On-demand analysis of the current position.
- Path: `session_id`
- 200: AnalysisResponse
- 404: Unknown session
- 500: Analysis failed

Example:
```bash
curl http://localhost:8000/analyze/SESSION_ID
```

### WebSocket `/ws/{session_id}`
Real‑time evaluation stream for the current position.
- Connect to: `ws://localhost:8000/ws/SESSION_ID`
- Server sends AnalysisResponse JSON periodically (~1s)

Example (browser):
```js
const ws = new WebSocket('ws://localhost:8000/ws/SESSION_ID');
ws.onmessage = (e) => {
  const analysis = JSON.parse(e.data);
  console.log(analysis);
};
```

### POST `/review_pgn`
Upload a PGN for engine review. Supports quick mode (faster).
- Content-Type: `multipart/form-data`
- Form fields:
  - `pgn_file`: file
  - `quick_mode`: boolean (optional; query or form; default false)
- 200: PgnReviewResponse
- 500: Failed to review PGN

Example:
```bash
curl -X POST "http://localhost:8000/review_pgn?quick_mode=true" \
  -H "Content-Type: multipart/form-data" \
  -F "pgn_file=@/path/to/game.pgn"
```

### POST `/resign/{session_id}`
Resign the game for the user. Board is not altered; result/status are overridden.
- 200: GameStateResponse

Example:
```bash
curl -X POST http://localhost:8000/resign/SESSION_ID
```

### POST `/restart/{session_id}`
Restart the current session to the initial position; user color is randomized again. If user becomes black, engine plays the first move.
- 200: GameStateResponse

Example:
```bash
curl -X POST http://localhost:8000/restart/SESSION_ID
```

## Errors

Errors return JSON:
```json
{ "detail": "Message" }
```
Common:
- 404 Session not found
- 500 Engine/analysis errors

## Notes on Engine and Depth

- The engine binary path is resolved via `STOCKFISH_PATH` or the system PATH (`stockfish`).
- PGN review:
  - quick mode depth ≈ 10
  - normal mode depth ≈ 20
- WebSocket analysis depth is the engine’s configured default (implementation may vary by build/settings).

## Versioning

This is an evolving API; fields may be extended in minor versions without breaking changes.
