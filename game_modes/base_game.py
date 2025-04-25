from grid import GridManager
from player import AIPlayer

class BaseGame:
    def __init__(self, size, words, mode="Classic"):
        self.mode = mode
        self.grid_manager = GridManager(size, words)
        self.ai = AIPlayer()
        self.words = set(words)
        self.found_words = set()
        self.turn = "Human"
        self.scores = {"human": 0, "ai": 0}

    def check_and_update_word(self, word, positions):
        if word in self.words and word not in self.found_words:
            self.found_words.add(word)
            self.grid_manager.reshuffle(positions, word)
            self.scores["human"] += 1
            return True
        return False

    def ai_turn(self):
        for word in self.words - self.found_words:
            path = self.ai.find_word(self.grid_manager.grid, word)
            if path:
                self.found_words.add(word)
                self.grid_manager.reshuffle(set(path), word)
                self.scores["ai"] += 1
                return word, path
        return None, None

    def get_score(self, player):
        return self.scores.get(player.lower(), 0)

    def is_game_over(self):
        return self.words == self.found_words
