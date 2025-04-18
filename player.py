class AIPlayer:
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (1, 1)]  # Right, Down, Diagonal

    def find_word(self, grid, word):
        size = len(grid)

        def dfs(r, c, index, dr=None, dc=None, path=None):
            if path is None:
                path = []

            if index == len(word):
                return path

            if not (0 <= r < size and 0 <= c < size) or grid[r][c] != word[index]:
                return None

            path.append((r, c))

            if dr is not None:
                # Continue in the same direction
                return dfs(r + dr, c + dc, index + 1, dr, dc, path)
            else:
                # Try all allowed directions from the first letter
                for new_dr, new_dc in self.directions:
                    result = dfs(r + new_dr, c + new_dc, index + 1, new_dr, new_dc, path.copy())
                    if result:
                        return result

            return None

        for r in range(size):
            for c in range(size):
                if grid[r][c] == word[0]:
                    result = dfs(r, c, 0)
                    if result:
                        return result

        return None
