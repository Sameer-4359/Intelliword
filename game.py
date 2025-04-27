from grid import GridManager
from player import AIPlayer
import time
import random
import pygame
from pygame import mixer

pygame.init()
pygame.mixer.init()

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

        # word chain
        if self.mode == "Word Chain":
            self.word_chain = list(words)  # keep order
            self.chain_index = 0


        # Grid Shuffle (optional)
        if self.mode == "Grid Shuffle":
            self.shuffle_interval = 10  # seconds
            self.last_shuffle_time = time.time()
        
        # Fog of War variables
        self.reveal_points = 2  # Starting reveal points
        self.revealed_cells = set()  # Track revealed positions
    
        # Initialize fog for Fog of War mode
        if self.mode == "Fog of War":
            self.initialize_fog()

    def check_and_update_word(self, word, positions):
        if self.mode == "Word Chain":
            # Only accept the current expected word
            if self.chain_index < len(self.word_chain) and word == self.word_chain[self.chain_index]:
                self.found_words.add(word)
                self.chain_index += 1
                self.scores["human"] += 1
                return True
            return False
        if self.mode == "Fog of War":
            for (r, c) in positions:
                if (r, c) not in self.revealed_cells:
                    print("✘ Can't select hidden cells!")
                    return False

        if word in self.words and word not in self.found_words:
            self.found_words.add(word)
            if self.mode == "Grid Shuffle":
                self.grid_manager.reshuffle(positions, word)

            self.scores["human"] += 1

            if self.mode == "Word Bomb" and self.bomb_word == word:
                self.bomb_word = None
                self.bomb_start_time = None
            
            if self.mode == "Fog of War":
                self.reveal_points += 1
                print(f"Word found! +1 reveal point. Total: {self.reveal_points}")

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
                    mixer.Sound("music/click.mp3").play()

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
        if self.mode == "Word Chain":
            return self.chain_index >= len(self.word_chain)
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
            mixer.Sound("music/bomb.mp3").play()
            pygame.time.delay(2000)  # Wait for 2 seconds before continuing
            self.found_words.add(self.bomb_word)
            self.bomb_word = None
            self.bomb_start_time = None
            self.bomb_failed = True  # NEW: Trigger game over


    def update_shuffle_timer(self):
        if self.mode == "Grid Shuffle":
            now = time.time()
            if now - self.last_shuffle_time >= self.shuffle_interval:
                print("🔀 Grid shuffled!")
                mixer.Sound("music/shuffle.mp3").play()
                self.grid_manager.shuffle_grid()
                self.last_shuffle_time = now
    

    def initialize_fog(self):
   
        self.revealed_cells = set()

    def reveal_area(self, center_row, center_col):
   
        if self.reveal_points <= 0:
            return False
    
        revealed = False
        for r in range(max(0, center_row-1), min(self.grid_manager.size, center_row+2)):
            for c in range(max(0, center_col-1), min(self.grid_manager.size, center_col+2)):
                if (r, c) not in self.revealed_cells:
                    self.revealed_cells.add((r, c))
                    revealed = True
    
        if revealed:
            self.reveal_points -= 1
        return revealed

# Add this method to check if a position is revealed
    def is_revealed(self, row, col):
        if self.mode != "Fog of War":
            return True
        return (row, col) in self.revealed_cells
