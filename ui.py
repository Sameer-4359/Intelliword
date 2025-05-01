import pygame
import random
import sys
from pygame import mixer

pygame.init()
pygame.mixer.init()

def draw_grid(screen, grid, cell_size, font,game=None):
    rows = len(grid)
    cols = len(grid[0])

    # Calculate the origin point based on the screen size and grid size
    if cols <= 6:
        origin_x = (screen.get_width()) //cols
    elif cols <= 8:
        origin_x = (screen.get_width()) //cols
    else:
        origin_x = (screen.get_width()) //cols 

    origin_y = 100

    for r, row in enumerate(grid):
        for c, letter in enumerate(row):
            x = origin_x + c * cell_size
            y = origin_y + r * cell_size

            # Skip drawing if cell is hidden in Fog of War mode
            if game and game.mode == "Fog of War" and not game.is_revealed(r, c):
                # Draw fog (gray semi-transparent square)
                fog_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                fog_surface.fill((100, 100, 100, 200))
                screen.blit(fog_surface, (x, y))
                continue

            # Draw semi-transparent box
            cell_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            cell_surface.fill((255, 255, 255, 60))  # White with ~25% opacity
            screen.blit(cell_surface, (x, y))

            # # Draw border
            # pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), 2)

            # Draw letter
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            screen.blit(text, text_rect)

def draw_word_list(screen, found_words, all_words, font, cell_size, grid_size, text_color=(0, 0, 0), bomb_word=None, bomb_icon=None, chain_word=None, reveal_points=None):
    x = 950
    y = 200
    # y = grid_size * cell_size + 10
    line_height = 30
    words_per_row = 1

    for index, word in enumerate(all_words):
        color = (0, 200, 0) if word in found_words else text_color
        word_text = font.render(word, True, color)
        word_x = x + (index % words_per_row) * 180
        word_y = y + (index // words_per_row) * line_height
        screen.blit(word_text, (word_x, word_y))

        # If this word is the bomb word, draw the bomb icon next to it
        if bomb_word == word and bomb_icon:
            icon_x = word_x + word_text.get_width() + 5
            icon_y = word_y + (font.get_height() - bomb_icon.get_height()) // 2
            screen.blit(bomb_icon, (icon_x, icon_y))

        # reveal points of fog of war
        if reveal_points is not None:
            points_text = font.render(f"Reveals: {reveal_points}", True, (255, 255, 255))
            screen.blit(points_text, (x-60, y + line_height * (len(all_words) // words_per_row + 1)))
            

    if chain_word is not None:
        chain_text = font.render(f"Chain Word: {chain_word}", True, (255, 255, 255))
        screen.blit(chain_text, (x-60, y + line_height * (len(all_words) // words_per_row + 1)))



def get_cell_under_mouse(pos, cell_size, grid_size, screen):
    cols = grid_size
    if cols <= 6:
        origin_x = (screen.get_width()) //cols
    elif cols <= 8:
        origin_x = (screen.get_width()) //cols
    else:
        origin_x = (screen.get_width()) //cols 

    origin_y = 100

    x, y = pos
    col = (x - origin_x) // cell_size
    row = (y - origin_y) // cell_size

    if 0 <= row < grid_size and 0 <= col < grid_size:
        return row, col
    return None  # Outside the grid

def get_random_color():
    return random.choice([
        (255, 255, 0, 128),   # Yellow
        (0, 255, 255, 128),   # Cyan
        (255, 105, 180, 128), # Pink
        (144, 238, 144, 128), # Light Green
        (221, 160, 221, 128), # Plum
    ])

def draw_lines(screen, found_lines, cell_size, grid_size, game=None):
    ANIMATION_SPEED = 0.08

    cols = grid_size
    if cols <= 6:
        origin_x = (screen.get_width()) //cols
    elif cols <= 8:
        origin_x = (screen.get_width()) //cols
    else:
        origin_x = (screen.get_width()) //cols 

    origin_y = 100

    for line in found_lines:
        color = line['color']
        positions = line['positions']
        progress = line['progress']
        width = line.get('width', 30)
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        total = len(positions)
        max_cells = int(progress * total)

        # Collect points for the connecting line
        points = []
        for idx in range(max_cells):
            row, col = positions[idx]
            x = origin_x + col * cell_size + cell_size // 2
            y = origin_y + row * cell_size + cell_size // 2
            points.append((x, y))

        for point in points:
            pygame.draw.circle(surface, color, point, width // 2,)
        

        # Draw the connecting line if at least 2 points
        if len(points) >= 2:
            pygame.draw.lines(surface, color, False, points, width)
            # Draw circles at the end points
            # pygame.draw.circle(surface, color, points[0], width // 2,)
            # pygame.draw.circle(surface, color, points[len(points)], width // 2,)
        screen.blit(surface, (0, 0))

        # Animate the progress
        if line['progress'] < 1.0:
            line['progress'] = min(1.0, line['progress'] + ANIMATION_SPEED)

# victory screen
def show_victory_screen(screen):
    mixer.music.load("music/winner.mp3")
    mixer.music.play()
    # Load fonts
    big_font = pygame.font.SysFont('Arial', 80, bold=True)
    small_font = pygame.font.SysFont('Arial', 40)

    # Render text
    victory_text = big_font.render("Congratulations!", True, (0, 128, 0))
    sub_text = small_font.render("You found all the words!", True, (255, 255, 255))

    # Get rects to center text
    victory_rect = victory_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    sub_rect = sub_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))

    # Draw text
    screen.blit(victory_text, victory_rect)
    screen.blit(sub_text, sub_rect)

    pygame.display.flip()

    # Wait for user to press key or mouse click
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        clock.tick(30)
