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

    