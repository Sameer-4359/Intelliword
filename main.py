import pygame
from game import Game
from ui import draw_grid, draw_word_list, get_cell_under_mouse, get_random_color, draw_lines
from menu import select_difficulty

def run_game():
    pygame.init()
    pygame.font.init()

    # Constants
    CELL_SIZE = 60
    FONT = pygame.font.SysFont('Arial', 28)
    WINDOW_SIZE = 600
    WORDS = ["CAT", "DOG", "SUN"]

    #initialize the title and icon and background
    pygame.display.set_caption("IntelliWord")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    background = pygame.image.load("background.jpg")
    newSize = (WINDOW_SIZE, WINDOW_SIZE + 100)
    background = pygame.transform.scale(background, newSize)

    # Menu
    screen = pygame.display.set_mode((600, 500))  # Set size temporarily for menu
    GRID_SIZE, max_word_length = select_difficulty(screen)

    # Set up display
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))  # extra space for word list

    # Game setup
    game = Game(size=GRID_SIZE, words=WORDS)

    #initialize the timer
    start_ticks = pygame.time.get_ticks()
    font = pygame.font.SysFont('Arial', 24)

    

    overFont = pygame.font.Font('freesansbold.ttf', 64)
    def showGameOver():
        game_over = overFont.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over, (100, 250))

    # Game loop
    running = True
    selected_start = None
    selected_end = None
    found_lines = [] # Each item: { 'start': (r, c), 'end': (r, c), 'progress': 0.0, 'color': (r, g, b) }
    game_completed = False


    while running:
        screen.blit(background, (0,0))

        draw_grid(screen, game.grid_manager.grid, CELL_SIZE, FONT)
        draw_word_list(screen, game.found_words, game.words, FONT, CELL_SIZE, GRID_SIZE)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_cell_under_mouse(pos, CELL_SIZE, GRID_SIZE, screen)
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    selected_start = (row, col)

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                row, col = get_cell_under_mouse(pos, CELL_SIZE, GRID_SIZE, screen)
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    selected_end = (row, col)

                    if selected_start and selected_end:
                        word, positions = game.grid_manager.get_word_from_coords(
                            selected_start, selected_end
                        )
                        if game.check_and_update_word(word, positions):
                            print(f"✔ You found: {word}")
                            positions = list(positions)   
                            found_lines.append({
                                'positions': positions,  # list of (row, col)
                                'progress': 0.0,
                                'color': get_random_color()
                            })
                            if set(game.found_words) == set(game.words):
                                game_completed = True

                        else:
                            print("✘ Not a valid word.")
                        selected_start = selected_end = None
        

        # Update found lines
        draw_lines(screen, found_lines, CELL_SIZE, GRID_SIZE)

        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = font.render(f"Time: {elapsed_seconds}s", True, (0, 0, 0))
        screen.blit(timer_text, (screen.get_width() - 100, 650))

        # Check if game is completed
        if game_completed and all(line['progress'] >= 1.0 for line in found_lines):
            showGameOver()
            pygame.display.flip()
            # Mini loop for a smooth 1.5 sec display
            end_time = pygame.time.get_ticks() + 1500
            while pygame.time.get_ticks() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                pygame.time.delay(10)

            print("🎉 All words found! Returning to menu...")
            running = False


        pygame.time.delay(10)
        pygame.display.flip()
        

while 1:
    run_game()   