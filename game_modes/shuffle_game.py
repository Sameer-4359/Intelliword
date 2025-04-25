import time
from game_modes.base_game import BaseGame

class ShuffleGame(BaseGame):
    def __init__(self, size, words):
        super().__init__(size, words, mode="Grid Shuffle")
        self.shuffle_interval = 10  # seconds
        self.last_shuffle_time = time.time()

    def update_shuffle_timer(self):
        now = time.time()
        if now - self.last_shuffle_time >= self.shuffle_interval:
            print("🔀 Grid shuffled!")
            self.grid_manager.shuffle_grid()
            self.last_shuffle_time = now
