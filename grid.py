import random
import string

class GridManager:
    def __init__(self, size, words):
        self.size = size
        self.words = words
        self.grid = [["*" for _ in range(size)] for _ in range(size)]
        self.found_positions = set()  # NEW: To store all locked positions
        self.place_words()
        self.fill_random_letters()

    def print_grid(self):
        for row in self.grid:
            print(" ".join(row))

    def place_words(self):
        directions = [(1, 0), (0, 1), (1, 1)]
        unplaced_words = []

        for word in self.words:
            placed = False
            for _ in range(100):
                row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                dr, dc = random.choice(directions)
                end_row = row + dr * (len(word) - 1)
                end_col = col + dc * (len(word) - 1)

                if 0 <= end_row < self.size and 0 <= end_col < self.size:
                    positions = [(row + i * dr, col + i * dc) for i in range(len(word))]
                    # NEW: Check if any of these are found_positions
                    if any(pos in self.found_positions for pos in positions):
                        continue

                    valid = all(self.grid[r][c] in ['*', word[i]]
                                for i, (r, c) in enumerate(positions))
                    if valid:
                        for i, (r, c) in enumerate(positions):
                            self.grid[r][c] = word[i]
                        placed = True
                        break
            if not placed:
                unplaced_words.append(word)

        return unplaced_words

    def fill_random_letters(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == "*":
                    self.grid[r][c] = random.choice(string.ascii_uppercase)

    def reshuffle(self, found_positions, found_word):
        # NEW: Update all-time found positions
        self.found_positions.update(found_positions)

        # Clear only non-found positions
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in self.found_positions:
                    self.grid[r][c] = "*"

        # Update word list
        self.words = [w for w in self.words if w != found_word]

        self.place_words()
        self.fill_random_letters()

    def get_word_from_coords(self, start, end):
        sr, sc = start
        er, ec = end
        word = ""
        positions = []

        dr = er - sr
        dc = ec - sc
        length = max(abs(dr), abs(dc)) + 1

        dr = 0 if dr == 0 else dr // abs(dr)
        dc = 0 if dc == 0 else dc // abs(dc)

        for i in range(length):
            r = sr + dr * i
            c = sc + dc * i
            if not (0 <= r < self.size and 0 <= c < self.size):
                return "", []
            word += self.grid[r][c]
            positions.append((r, c))

        return word, set(positions)
