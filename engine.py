import subprocess

class StockfishEngine:
    def __init__(self):
        #get the stockfish path, (use .exe for windows devices)
        executable = 'stockfish_binary/stockfish'
        
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
        self.engine.stdin.write('uci/n') 
        self.engine.stdin.flush()

        #making sure its ready
        self.engine.stdin.write('isready\n')
        self.engine.stdin.flush()


        #waiting for uciok and readyok response
        self.read_until('uciok')
        self.read_until('readyok')

    def read_until(self, keyword):
        while True:
            line = self.engine.stdout.readline().strip()
            if keyword in line:
                break

