# NoChess.com

A modern chess web app with a React frontend and FastAPI backend powered by Stockfish. Play against the engine, see real‑time evaluations, run on‑demand analysis, and unlimited review (unlike chess.com's paywall) for PGN files with chess.com‑style review comments.

- Frontend: React (Vite) + react-chessboard
- Backend: FastAPI + python‑chess + Stockfish
- Live evaluation: WebSocket stream
- PGN review: quick mode or full review with comments

For full API reference, see the API documentation:
- API docs: [API_DOCUMENTATION](API_DOCUMENTATION.md)

## Features

- Play vs AI (engine replies automatically)
- Real-time evaluation bar via WebSocket
- On-demand analysis (best move, PV, depth)
- PGN review with “Brilliant/Mistake/Blunder/…” comments
- Resign and restart controls
- Random user color assignment (white/black) on start/restart
- Robust game state: FEN, status flags, last move, legal moves

## Architecture

- Frontend (default: http://localhost:5173)
  - React + Vite, chessboard UI, WebSocket evaluation bar
- Backend (default: http://localhost:8000)
  - FastAPI service, Stockfish engine controller, session manager
- Engine
  - Stockfish (resolved via STOCKFISH_PATH or found in PATH)

CORS is enabled for the frontend origin(s) on 5173.

## Prerequisites

- Node.js 18+ and npm (or pnpm/yarn)
- Python 3.10+
- Stockfish chess engine installed and accessible:
  - macOS: `brew install stockfish`
  - Ubuntu/Debian: `sudo apt-get install stockfish`
  - Windows: install and add to PATH (Scoop/Choco or manual)
- Optional: Docker/Docker Compose (if you prefer containers)

Set the engine path if not in PATH:
- macOS/Linux: `export STOCKFISH_PATH=/usr/local/bin/stockfish`
- Windows (PowerShell): `$env:STOCKFISH_PATH="C:\\path\\to\\stockfish.exe"`

## Configuration

Frontend (Vite):
- `VITE_API_BASE_URL` (optional; default `http://localhost:8000`)
- `VITE_WS_BASE_URL` (optional; default `ws://localhost:8000`)

Backend:
- `STOCKFISH_PATH` (optional; default `stockfish` in PATH)

## Getting Started (Local Dev)

1) Backend
- Create and activate a virtual environment (recommended)
- Install dependencies (example):
  ```bash
  pip install fastapi uvicorn python-chess
  ```
  If you have a `requirements.txt`, use:
  ```bash
  pip install -r requirements.txt
  ```
- Run the server:
  ```bash
  uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
  ```
  The backend will resolve Stockfish from `STOCKFISH_PATH` or PATH.

2) Frontend
- From the frontend directory:
  ```bash
  npm install
  npm run dev
  ```
- Open http://localhost:5173

## Docker (Optional)

If you have a Dockerfile for the backend:
```bash
docker build -t nochess-backend .
docker run --rm -p 8000:8000 \
  -e STOCKFISH_PATH=/usr/bin/stockfish \
  nochess-backend
```

Ensure the container has Stockfish installed (either in the image or mounted).

## Project Structure (typical)

```
backend/
  app.py
  engine.py
  chess_game.py
  models.py
  pgnReview.py
  utils.py
  ui/terminal_ui.py
frontend/
  src/
    components/
    styles/
    api.js (or api/index.js)
```

## Development Notes

- The engine is analyzed at a configurable depth internally. The WebSocket stream emits the latest analysis ~1s cadence.
- PGN review supports quick mode (faster, lower depth) and normal mode (deeper).
- In headless environments (e.g., Docker), terminal UI calls are automatically disabled to avoid TERM warnings.

## Troubleshooting

- Engine not found
  - Set `STOCKFISH_PATH` or install Stockfish into PATH.
- WebSocket disconnects
  - Ensure `VITE_WS_BASE_URL` matches the backend host and protocol (`ws://` for local, `wss://` for TLS).

## License

Add your license here.

## Acknowledgements

- [python-chess](https://python-chess.readthedocs.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [react-chessboard](https://github.com/Clariity/react-chessboard)
- Stockfish authors and contributors
