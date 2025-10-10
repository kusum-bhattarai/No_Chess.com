import subprocess
import select
import time
import re
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class StockfishEngine:
    def __init__(self, mode: str = "intermediate", executable_path: str = None):

        self.executable_path = executable_path or os.getenv("STOCKFISH_PATH", "stockfish_binary/stockfish")
        
        #modes mapped to depths
        depth_map = {
            "beginner": 8,
            "intermediate": 12,
            "advanced": 16
        }

        skill_map = {
            "beginner": 5,
            "intermediate": 10,
            "advanced": 20
        }

        self.depth = depth_map.get(mode, 10) #10 in case mode is unrecognized
        self.skill = skill_map.get(mode, 10) #10 in case not recognized

        # Validate binary
        self._validate_binary()

        # Launch process
        self.engine = subprocess.Popen(
            [self.executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )

        self._send_command('uci')
        self._wait_for_response('uciok')

        self.set_skill_level()

        self._send_command('isready')
        self._wait_for_response('readyok')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.terminate()
            self.engine.wait(timeout=5)
        return False  # Re-raise exceptions if any

    def _validate_binary(self):
        """Validate Stockfish binary exists and is version 17.1 via 'uci' command."""
        try:
            # Run 'uci' to get version output
            result = subprocess.run(
                [self.executable_path],
                input='uci\n',
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0 or 'Stockfish 17.1' not in result.stdout:
                raise OSError(f"Invalid or missing Stockfish binary at {self.executable_path}. Expected version 17.1. Download from https://stockfishchess.org/download/")
        except FileNotFoundError:
            raise OSError(f"Stockfish binary not found at {self.executable_path}. Download from https://stockfishchess.org/download/")
        except subprocess.TimeoutExpired:
            raise OSError(f"Stockfish binary at {self.executable_path} timed out. Check if it's valid.")

    def _send_command(self, command: str):
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()

    def _wait_for_response(self, keyword: str, timeout: int = 30):
        """Wait for response with timeout using select."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            ready, _, _ = select.select([self.engine.stdout], [], [], 1)
            if ready:
                line = self.engine.stdout.readline().strip()
                if keyword in line:
                    return line
            time.sleep(0.1)
        raise TimeoutError(f"Timeout waiting for '{keyword}' response")

    def set_position(self, moves: List[str]):
        command = "position startpos"
        if moves:
            moves_str = " ".join(moves)
            command += f" moves {moves_str}"
        self._send_command(command)

    def set_skill_level(self):
        self._send_command(f"setoption name Skill Level value {self.skill}")

    def get_best_move(self):
        self._send_command(f"go depth {self.depth}")
        return self._parse_best_move()

    def _parse_best_move(self):
        while True:
            line = self._read_line_with_timeout()
            if line.startswith("bestmove"):
                parts = line.split()
                return parts[1] if len(parts) >= 2 else None

    def analyze_position(self, depth: int = 20) -> Dict:
        self._send_command(f"go depth {depth}")
        analysis = {
            "score": 0,
            "is_mate": False,
            "best_move": None,
            "pv": [],
            "depth": 0
        }
        while True:
            line = self._read_line_with_timeout()
            if line.startswith("info depth"):
                analysis.update(self._parse_info_line(line))
            elif line.startswith("bestmove"):
                parts = line.split()
                analysis["best_move"] = parts[1] if len(parts) >= 2 else None
                break
        return analysis

    def _read_line_with_timeout(self, timeout: int = 30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            ready, _, _ = select.select([self.engine.stdout], [], [], 1)
            if ready:
                line = self.engine.stdout.readline().strip()
                if line:
                    return line
            time.sleep(0.1)
        raise TimeoutError("Timeout reading from engine")

    def _parse_info_line(self, line: str) -> Dict:
        """Parse info line with regex for robustness."""
        depth_match = re.search(r'depth (\d+)', line)
        score_match = re.search(r'score (cp|mate) ([-+]?\d+)', line)
        pv_match = re.search(r'pv (.*)', line)

        parsed = {"depth": int(depth_match.group(1)) if depth_match else 0}

        if score_match:
            score_type, score_value = score_match.groups()
            score_val = int(score_value)
            parsed["is_mate"] = score_type == "mate"
            parsed["score"] = score_val
        if pv_match:
            parsed["pv"] = pv_match.group(1).split() if pv_match.group(1) else []

        return parsed