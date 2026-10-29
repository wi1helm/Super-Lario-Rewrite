import time
from datetime import datetime

class Glogger:
    def __init__(self, flush_rate=2):
        self.flush_rate = flush_rate
        self.last_flush = time.time()
        self.buffer = []  # list preserves order

    def add(self, level, message):
        if message not in self.buffer:

            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            message = f"{message} | {timestamp}"
            self.buffer.append((level, message))

    def log(self, message):
        self.add("LOG", message)
        
    def warning(self, message):
        self.add("WARNING", message)

    def error(self, message):
        self.add("ERROR", message)

    def flush(self):
        now = time.time()
        delta = now - self.last_flush

        if delta < 1 / self.flush_rate:
            return


        for level, msg in self.buffer:
            print(f"[{level}] {msg} (+{delta:.2f}s)")

        self.buffer.clear()
        self.last_flush = now
    
    def flush_all(self):
        for level, msg in self.buffer:
            print(f"[{level}] {msg}")

        self.buffer.clear()
