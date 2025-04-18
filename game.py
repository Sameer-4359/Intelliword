from grid import GridManager
from player import AIPlayer

class Game:
    def __init__(self, size, words):
        self.grid_manager = GridManager(size, words)
        self.ai = AIPlayer()
        self.words = set(words)
        self.found_words = set()
        self.turn = "Human"  # start with human

    def check_and_update_word(self, word, positions):
        if word in self.words and word not in self.found_words:
            self.found_words.add(word)
            self.grid_manager.reshuffle(positions, word)
            return True
        return False

    def ai_turn(self):
        """Performs a single AI move if a word can be found."""
        for word in self.words - self.found_words:
            path = self.ai.find_word(self.grid_manager.grid, word)
            if path:
                self.found_words.add(word)
                self.grid_manager.reshuffle(set(path), word)
                return word, path
        return None, None

    def is_game_over(self):
        return self.words == self.found_words
