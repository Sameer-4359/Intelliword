from game_modes.base_game import BaseGame

class ClassicGame(BaseGame):
    def __init__(self, size, words):
        super().__init__(size, words, mode="Classic")
