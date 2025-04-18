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

def directional_dfs_ai(grid, word):
    directions = [(0, 1), (1, 0), (1, 1)]  # Right, Down, Diagonal
    size = len(grid)
    word_len = len(word)

    def dfs(r, c, index, dr=None, dc=None, path=[]):
        if index == len(word):
            return path

        if not (0 <= r < size and 0 <= c < size):
            return None

        if grid[r][c] != word[index]:
            return None

        path.append((r, c))

        if dr is not None and dc is not None:
            # Continue in the given direction
            return dfs(r + dr, c + dc, index + 1, dr, dc, path)
        else:
            # Try all 3 directions from the first letter
            for new_dr, new_dc in directions:
                result = dfs(r + new_dr, c + new_dc, index + 1, new_dr, new_dc, path.copy())
                if result:
                    return result

        return None

    for row in range(size):
        for col in range(size):
            if grid[row][col] == word[0]:
                found_path = dfs(row, col, 0, None, None, [])
                if found_path:
                    return found_path

    return None


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
# while len(found_words) < len(words):
#     print("\nWords to find:", [w for w in words if w not in found_words])
#     print("Enter start and end coordinates (or type 'exit' to stop):")

#     user_input = input("Start Row (or 'exit'): ").strip()
#     if user_input.lower() == "exit":
#         print("Game exited.")
#         break

#     try:
#         sr = int(user_input)
#         sc = int(input("Start Col: "))
#         er = int(input("End Row: "))
#         ec = int(input("End Col: "))

#         selected_word, selected_positions = get_word_from_coords(grid, (sr, sc), (er, ec))
#         print(f"\nYou selected: {selected_word}")

#         if selected_word in words and selected_word not in found_words:
#             print("✔ Correct Word!")
#             found_words.add(selected_word)

#             # Reshuffle the grid with the found word preserved
#             unplaced_after = reshuffle_grid(grid, selected_positions, words, selected_word)

#             print("\nGrid After Reshuffling:")
#             print_grid(grid)

#             if unplaced_after:
#                 print("\nCould not place these words after reshuffling:", unplaced_after)
#         else:
#             print("✘ Invalid or already found.")

#     except ValueError:
#         print("❌ Invalid input. Please enter integers for coordinates.")

# if len(found_words) == len(words):
#     print("\n🎉 Congratulations! You found all the words!")

# --- Let AI Try to Find a Word ---
# print("\n🤖 AI is trying to find a word...")
# for w in words:
#     if w not in found_words:
#         path = directional_dfs_ai(grid, w)
#         if path:
#             print(f"🤖 AI found the word '{w}' at positions: {path}")
#             found_words.add(w)

#             # Reshuffle the grid after AI finds a word
#             unplaced_after = reshuffle_grid(grid, set(path), words, w)

#             print("\nGrid After AI Found Word and Reshuffling:")
#             print_grid(grid)

#             if unplaced_after:
#                 print("\nCould not place these words after reshuffling:", unplaced_after)
#         else:
#             print(f"🤖 AI could not find the word '{w}'")

# --- AI and Human Turn-Based Game Loop ---
turn = "AI"  # Start with AI

while len(found_words) < len(words):
    print("\nWords to find:", [w for w in words if w not in found_words])
    
    if turn == "AI":
        print("\n🤖 AI is thinking...")
        move_made = False

        for w in words:
            if w not in found_words:
                path = directional_dfs_ai(grid, w)
                if path:
                    print(f"🤖 AI found the word '{w}' at positions: {path}")
                    found_words.add(w)
                    move_made = True

                    # Reshuffle grid with AI found word preserved
                    unplaced_after = reshuffle_grid(grid, set(path), words, w)
                    print("\nGrid After AI Found Word and Reshuffling:")
                    print_grid(grid)

                    if unplaced_after:
                        print("\nCould not place these words after reshuffling:", unplaced_after)
                    break  # Only one move per turn
        if not move_made:
            print("🤖 AI could not find any word.")

        turn = "Human"  # Switch turn

    else:  # Human turn
        print("\n🧍 Human's Turn:")
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

                # Reshuffle grid with human-found word preserved
                unplaced_after = reshuffle_grid(grid, selected_positions, words, selected_word)

                print("\nGrid After Human Found Word and Reshuffling:")
                print_grid(grid)

                if unplaced_after:
                    print("\nCould not place these words after reshuffling:", unplaced_after)
            else:
                print("✘ Invalid or already found.")

        except ValueError:
            print("❌ Invalid input. Please enter integers for coordinates.")
        
        turn = "AI"  # Switch turn

if len(found_words) == len(words):
    print("\n🎉 Game Over! All words have been found!")

