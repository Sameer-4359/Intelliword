import random
import string

def generate_grid(size):
    """Generates a grid filled with '*' characters initially."""
    grid = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append("*")  # Placeholder for empty spaces
        grid.append(row)
    return grid

def print_grid(grid):
    """Prints the grid in a readable format."""
    for row in grid:
        print(" ".join(row))

def place_words(grid, words, size):
    """Attempts to place multiple words in the grid."""
    directions = [(1, 0), (0, 1), (1, 1)]  # Right, Down, Diagonal
    unplaced_words = []  # Store words that couldn't be placed

    for word in words:
        word_length = len(word)
        placed = False  # Track if the word was placed

        for _ in range(100):  # Try multiple times
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            dr, dc = random.choice(directions)

            end_row = row + dr * (word_length - 1)
            end_col = col + dc * (word_length - 1)

            if 0 <= end_row < size and 0 <= end_col < size:
                valid_position = True
                for i in range(word_length):
                    current_row = row + i * dr
                    current_col = col + i * dc
                    current_cell = grid[current_row][current_col]

                    if current_cell not in [word[i], "*"]:
                        valid_position = False
                        break

                if valid_position:
                    for i in range(word_length):
                        grid[row + i * dr][col + i * dc] = word[i]
                    placed = True
                    break  # Exit placement loop if word is placed

        if not placed:
            unplaced_words.append(word)  # Store unplaced words

    return unplaced_words  # Return list of words that couldn't be placed

def fill_random_letters(grid, size):
    """Fills remaining '*' cells with random letters."""
    for row in range(size):
        for col in range(size):
            if grid[row][col] == "*":
                grid[row][col] = random.choice(string.ascii_uppercase)
    

def reshuffle_grid(grid, found_positions, words, found_word):
    """Clears non-found words, then places them again while keeping found words untouched."""
    size = len(grid)
    
    # Extract remaining words that need to be placed again
    remaining_words = [word for word in words if word != found_word]

    # Clear only the non-found words from the grid
    for r in range(size):
        for c in range(size):
            if (r, c) not in found_positions:
                grid[r][c] = "*"

    # Reassign the remaining words
    unplaced_words = place_words(grid, remaining_words, size)

    # Fill remaining empty spaces with random letters
    fill_random_letters(grid, size)

    return unplaced_words  # Return words that couldn't be placed








# --- Testing the functions ---
size = 5  # Grid size
grid = generate_grid(size)

# List of words to place
words = ["CAT", "DOG", "SUN"]

# Place words in the grid
unplaced = place_words(grid, words, size)

# Fill remaining empty spaces with random letters
fill_random_letters(grid, size)

# Print the initial grid
print("\nInitial Grid:")
print_grid(grid)

# Simulate finding a word (e.g., "CAT" at specific positions)
found_word = "CAT"
found_positions = {(0, 0), (0, 1), (0, 2)}  # Assume we found "CAT" at these positions

# Reshuffle the grid while keeping found words intact
unplaced_after_shuffle = reshuffle_grid(grid, found_positions, words, found_word)

# Print the final grid after reshuffling
print("\nGrid After Reshuffling:")
print_grid(grid)

# Print unplaced words (if any)
if unplaced_after_shuffle:
    print("\nCould not place these words after reshuffling:", unplaced_after_shuffle)
