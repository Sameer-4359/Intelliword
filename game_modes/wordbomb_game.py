import pygame
import random
from game_modes.base_game import BaseGame

class WordBombGame(BaseGame):
    def __init__(self, size, words):
        super().__init__(size, words, mode="Word Bomb")
        self.bomb_word = None
        self.bomb_start_time = None
        self.bomb_interval = 5000  # milliseconds
        self.bomb_duration = 10  # seconds
        self.last_bomb_time = pygame.time.get_ticks()

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

    def check_and_update_word(self, word, positions):
        success = super().check_and_update_word(word, positions)
        if success and self.bomb_word == word:
            self.bomb_word = None
            self.bomb_start_time = None
        return success

    def ai_turn(self):
        word, path = super().ai_turn()
        if word and self.bomb_word == word:
            self.bomb_word = None
            self.bomb_start_time = None
        return word, path
