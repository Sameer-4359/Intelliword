import random
import string

def generate_grid(size):
    grid = [["*" for _ in range(size)] for _ in range(size)]
    return grid

def print_grid(grid):
    for row in grid:
        print(" ".join(row))

def place_words(grid, words, size):
    directions = [(1, 0), (0, 1), (1, 1)]  # Right, Down, Diagonal
    unplaced_words = []

    for word in words:
        word_length = len(word)
        placed = False

        for _ in range(100):
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
                    break

        if not placed:
            unplaced_words.append(word)

    return unplaced_words

def fill_random_letters(grid, size):
    for row in range(size):
        for col in range(size):
            if grid[row][col] == "*":
                grid[row][col] = random.choice(string.ascii_uppercase)

def reshuffle_grid(grid, found_positions, words, found_word):
    size = len(grid)
    remaining_words = [word for word in words if word != found_word]

    for r in range(size):
        for c in range(size):
            if (r, c) not in found_positions:
                grid[r][c] = "*"

    unplaced_words = place_words(grid, remaining_words, size)
    fill_random_letters(grid, size)
    return unplaced_words

def get_word_from_coords(grid, start, end):
    """Extract the word from grid using start and end (row, col) coordinates."""
    sr, sc = start
    er, ec = end
    word = ""
    positions = []

    dr = er - sr
    dc = ec - sc
    length = max(abs(dr), abs(dc)) + 1

    # Normalize direction to unit steps
    dr = 0 if dr == 0 else dr // abs(dr)
    dc = 0 if dc == 0 else dc // abs(dc)

    for i in range(length):
        r = sr + dr * i
        c = sc + dc * i
        if 0 <= r < len(grid) and 0 <= c < len(grid):
            word += grid[r][c]
            positions.append((r, c))
        else:
            return "", []  # Out of bounds

    return word, set(positions)

size = 5
grid = generate_grid(size)
words = ["CAT", "DOG", "SUN"]
found_words = set()

# Place and fill the grid
unplaced = place_words(grid, words, size)
fill_random_letters(grid, size)

print("\nInitial Grid:")
print_grid(grid)

# --- Game Loop for Player Word Selection ---
while len(found_words) < len(words):
    print("\nWords to find:", [w for w in words if w not in found_words])
    print("Enter start and end coordinates (or type 'exit' to stop):")

    user_input = input("Start Row (or 'exit'): ").strip()
    if user_input.lower() == "exit":
        print("Game exited.")
        break

    try:
        sr = int(user_input)
        sc = int(input("Start Col: "))
        er = int(input("End Row: "))
        ec = int(input("End Col: "))

        selected_word, selected_positions = get_word_from_coords(grid, (sr, sc), (er, ec))
        print(f"\nYou selected: {selected_word}")

        if selected_word in words and selected_word not in found_words:
            print("✔ Correct Word!")
            found_words.add(selected_word)

            # Reshuffle the grid with the found word preserved
            unplaced_after = reshuffle_grid(grid, selected_positions, words, selected_word)

            print("\nGrid After Reshuffling:")
            print_grid(grid)

            if unplaced_after:
                print("\nCould not place these words after reshuffling:", unplaced_after)
        else:
            print("✘ Invalid or already found.")

    except ValueError:
        print("❌ Invalid input. Please enter integers for coordinates.")

if len(found_words) == len(words):
    print("\n🎉 Congratulations! You found all the words!")