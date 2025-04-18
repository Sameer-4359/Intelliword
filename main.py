import pygame
from game import Game
from ui import draw_grid, draw_word_list, get_cell_under_mouse

pygame.init()
pygame.font.init()

# Constants
CELL_SIZE = 60
FONT = pygame.font.SysFont('Arial', 28)
WINDOW_SIZE = 600
GRID_SIZE = 5
WORDS = ["CAT", "DOG", "SUN"]

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))  # extra space for word list
pygame.display.set_caption("IntelliWord")

# Game setup
game = Game(size=GRID_SIZE, words=WORDS)

# Game loop
running = True
selected_start = None
selected_end = None

while running:
    screen.fill((255, 255, 255))  # White background

    draw_grid(screen, game.grid_manager.grid, CELL_SIZE, FONT)
    draw_word_list(screen, game.found_words, game.words, FONT, CELL_SIZE, GRID_SIZE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_cell_under_mouse(pos, CELL_SIZE)
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                selected_start = (row, col)

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            row, col = get_cell_under_mouse(pos, CELL_SIZE)
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                selected_end = (row, col)

                if selected_start and selected_end:
                    word, positions = game.grid_manager.get_word_from_coords(
                        selected_start, selected_end
                    )
                    if game.check_and_update_word(word, positions):
                        print(f"✔ You found: {word}")
                    else:
                        print("✘ Not a valid word.")
                    selected_start = selected_end = None

    pygame.display.flip()

pygame.quit()
