import subprocess

class StockfishEngine:
    def __init__(self, mode="intermediate"):
        #get the stockfish path, (use .exe for windows devices)
        executable = 'stockfish_binary/stockfish'
        
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

        #launch the Stockfish process
        self.engine = subprocess.Popen(
            executable,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, 
            text=True,
            bufsize=1
        )

        #sending uci command
        self.engine.stdin.write('uci\n') 
        self.engine.stdin.flush()
        #wait for uciok response
        self.read_until('uciok')

        self.set_skill_level() #skill level set

        #making sure its ready
        self.engine.stdin.write('isready\n')
        self.engine.stdin.flush()
        #waiting for readyok response    
        self.read_until('readyok')


    def read_until(self, keyword):
        while True:
            line = self.engine.stdout.readline().strip()
            if keyword in line:
                break

    def set_position(self, moves: list):
        #construct the position command
        command = "position startpos"
        if moves:
            moves_str = " ".join(moves)
            command += f" moves {moves_str}"
        
        #send the command to stockfish
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()          

    def set_skill_level(self):
        self.engine.stdin.write(f"setoption name Skill Level value {self.skill}\n")
        self.engine.stdin.flush()


    def get_best_move(self):
        self.engine.stdin.write(f"go depth {self.depth}\n")
        self.engine.stdin.flush()

        best_move = None
        while True:
            line = self.engine.stdout.readline().strip()
            if line.startswith("bestmove"):
                parts = line.split()
                if len(parts) >= 2:
                    best_move = parts[1]
                break  # Exit after finding best move

        return best_move