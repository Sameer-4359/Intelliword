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

def draw_word_list(screen, found_words, all_words, font, cell_size, grid_size):
    cols = grid_size
    origin_x = (screen.get_width() - cols * cell_size) // 2
    origin_y = 100 if cols <= 6 else 50

    # Calculate y-position just below the grid
    y_offset = origin_y + grid_size * cell_size + 20
    x_offset = origin_x

    for word in all_words:
        color = (0, 0, 0) if word in found_words else (255, 255, 255)
        text = font.render(word, True, color)
        screen.blit(text, (x_offset, y_offset))
        x_offset += text.get_width() + 20


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
    ANIMATION_SPEED = 0.05  # Adjust for slower/faster animation

    cols = grid_size
    origin_x = (screen.get_width() - cols * cell_size) // 2
    origin_y = 100 if cols <= 6 else 50

    for line in found_lines:
        color = line['color']
        positions = line['positions']
        progress = line['progress']

        # Convert grid positions to screen coordinates with offset
        pixel_points = [
            (
                origin_x + col * cell_size + cell_size // 2,
                origin_y + row * cell_size + cell_size // 2
            )
            for row, col in positions
        ]

        total_segments = len(pixel_points) - 1
        if total_segments == 0:
            continue  # nothing to draw

        segments_to_draw = int(progress * total_segments)

        # Draw fully completed segments
        for i in range(segments_to_draw):
            pygame.draw.line(screen, color, pixel_points[i], pixel_points[i+1], 4)

        # Draw partially-progressed segment
        if segments_to_draw < total_segments:
            start_pt = pixel_points[segments_to_draw]
            end_pt = pixel_points[segments_to_draw + 1]
            segment_progress = (progress * total_segments) - segments_to_draw

            mid_x = int(start_pt[0] + (end_pt[0] - start_pt[0]) * segment_progress)
            mid_y = int(start_pt[1] + (end_pt[1] - start_pt[1]) * segment_progress)
            pygame.draw.line(screen, color, start_pt, (mid_x, mid_y), 4)

        # Update animation progress
        if line['progress'] < 1.0:
            line['progress'] = min(1.0, line['progress'] + ANIMATION_SPEED)

def get_random_color():
    return random.choice([
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 165, 0), (128, 0, 128), (0, 255, 255),
        (255, 105, 180), (255, 255, 0)
    ])
