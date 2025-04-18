import pygame
def draw_grid(screen, grid, cell_size, font):
    for r, row in enumerate(grid):
        for c, letter in enumerate(row):
            rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 0)  # fill
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)        # border

            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def draw_word_list(screen, found_words, all_words, font, cell_size, grid_size):
    x_offset = 10
    y_offset = grid_size * cell_size + 10
    for word in all_words:
        color = (0, 128, 0) if word in found_words else (128, 0, 0)
        text = font.render(word, True, color)
        screen.blit(text, (x_offset, y_offset))
        x_offset += text.get_width() + 20

def get_cell_under_mouse(pos, cell_size):
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    return row, col
