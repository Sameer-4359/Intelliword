from grid import GridManager
from player import AIPlayer
import time
import random
import pygame

class Game:
    def __init__(self, size, words, mode="Classic"):
        self.mode = mode
        self.grid_manager = GridManager(size, words)
        self.ai = AIPlayer()
        self.words = set(words)
        self.found_words = set()
        self.turn = "Human"
        self.scores = {"human": 0, "ai": 0}

        # Word Bomb mode variables
        self.bomb_word = None
        self.bomb_start_time = None
        self.bomb_duration = 10  # seconds
        self.bomb_trigger_interval = 30  # seconds
        self.last_bomb_time = time.time()
        self.bomb_failed = False  # NEW: To track if bomb failure should end game


        # Grid Shuffle (optional)
        if self.mode == "Grid Shuffle":
            self.shuffle_interval = 10  # seconds
            self.last_shuffle_time = time.time()

    def check_and_update_word(self, word, positions):
        if word in self.words and word not in self.found_words:
            self.found_words.add(word)
            # Only reshuffle in non-Word Bomb mode
            if self.mode == "Grid Shuffle":
                self.grid_manager.reshuffle(positions, word)

            self.scores["human"] += 1

            # Word Bomb cleared
            if self.mode == "Word Bomb" and self.bomb_word == word:
                self.bomb_word = None
                self.bomb_start_time = None

            return True
        return False

    def ai_turn(self):
        for word in self.words - self.found_words:
            path = self.ai.find_word(self.grid_manager.grid, word)
            if path:
                self.found_words.add(word)
                # Only reshuffle if we are in grid shuffle mode
                if self.mode == "Grid Shuffle":
                    self.grid_manager.reshuffle(set(path), word)

                self.scores["ai"] += 1

                # If AI defuses the bomb
                if self.mode == "Word Bomb" and self.bomb_word == word:
                    self.bomb_word = None
                    self.bomb_start_time = None

                return word, path
        return None, None

    def get_score(self, player):
        return self.scores.get(player.lower(), 0)

    def is_game_over(self):
        return self.words == self.found_words

    # ---- Word Bomb Methods ----
    def pick_random_unfound_word(self):
        remaining = list(self.words - self.found_words)
        if remaining:
            self.bomb_word = random.choice(remaining)
            self.bomb_start_time = pygame.time.get_ticks()

    def handle_bomb_failure(self):
        if self.bomb_word:
            print(f"💥 Bomb word missed: {self.bomb_word}")
            self.found_words.add(self.bomb_word)
            self.bomb_word = None
            self.bomb_start_time = None
            self.bomb_failed = True  # NEW: Trigger game over


    def update_shuffle_timer(self):
        if self.mode == "Grid Shuffle":
            now = time.time()
            if now - self.last_shuffle_time >= self.shuffle_interval:
                print("🔀 Grid shuffled!")
                self.grid_manager.shuffle_grid()
                self.last_shuffle_time = now
