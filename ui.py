import pygame
import random

def draw_grid(screen, grid, cell_size, font):
    rows = len(grid)
    cols = len(grid[0])

    # Calculate dynamic offsets
    origin_x = (screen.get_width() - cols * cell_size) // 2
    origin_y = 100 if cols <= 6 else 50

    for r, row in enumerate(grid):
        for c, letter in enumerate(row):
            x = origin_x + c * cell_size
            y = origin_y + r * cell_size

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

def draw_word_list(screen, found_words, all_words, font, cell_size, grid_size, text_color=(0, 0, 0), bomb_word=None, bomb_icon=None):
    x = 10
    y = grid_size * cell_size + 10
    line_height = 30
    words_per_row = 3

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



def get_cell_under_mouse(pos, cell_size, grid_size, screen):
    cols = grid_size
    origin_x = (screen.get_width() - cols * cell_size) // 2
    origin_y = 100 if cols <= 6 else 50

    x, y = pos
    col = (x - origin_x) // cell_size
    row = (y - origin_y) // cell_size

    if 0 <= row < grid_size and 0 <= col < grid_size:
        return row, col
    return None  # Outside the grid

def draw_lines(screen, found_lines, cell_size, grid_size):
    ANIMATION_SPEED = 0.05

    cols = grid_size
    origin_x = (screen.get_width() - cols * cell_size) // 2
    origin_y = 100 if cols <= 6 else 50

    for line in found_lines:
        color = line['color']
        positions = line['positions']
        progress = line['progress']
        opacity = line.get('opacity', 130)  # Slightly see-through like a highlighter

        # Create transparent surface for highlight
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        total = len(positions)
        max_cells = int(progress * total)

        for idx in range(max_cells):
            row, col = positions[idx]
            x = origin_x + col * cell_size
            y = origin_y + row * cell_size

            highlight_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            highlight_surface.fill((*color, opacity))
            surface.blit(highlight_surface, (x, y))

        # Animate partially appearing cell
        if max_cells < total:
            row, col = positions[max_cells]
            x = origin_x + col * cell_size
            y = origin_y + row * cell_size

            partial_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            partial_surface.fill((*color, int(opacity * (progress * total - max_cells))))
            surface.blit(partial_surface, (x, y))

        screen.blit(surface, (0, 0))

        # Progress animation
        if line['progress'] < 1.0:
            line['progress'] = min(1.0, line['progress'] + ANIMATION_SPEED)

def get_random_color():
    return random.choice([
        (255, 255, 0),   # Yellow
        (0, 255, 255),   # Cyan
        (255, 105, 180), # Pink
        (144, 238, 144), # Light Green
        (221, 160, 221), # Plum
    ])

