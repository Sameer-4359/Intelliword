import pygame
import sys

def select_difficulty(screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)

    modes = ["Classic", "Grid Shuffle", "Word Bomb", "Word Chain", "Fog of War"]  # Added Word Chain
    difficulties = [("Easy", 5, 5), ("Medium", 8, 8), ("Hard", 10, 10)]

    selected_mode = None
    selected_diff = None

    while not selected_mode:
        screen.fill((30, 30, 30))
        title = font.render("Select Game Mode", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))

        mode_rects = []
        for i, mode in enumerate(modes):
            rect = pygame.Rect(screen.get_width()//2 - 100, 150 + i*70, 200, 50)
            mode_rects.append((rect, mode))
            pygame.draw.rect(screen, (100, 180, 100), rect)
            text = small_font.render(mode, True, (0, 0, 0))
            screen.blit(text, (rect.x + 40, rect.y + 12))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, mode in mode_rects:
                    if rect.collidepoint(pos):
                        selected_mode = mode

    while not selected_diff:
        screen.fill((30, 30, 30))
        title = font.render("Select Difficulty", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))

        diff_rects = []
        for i, (label, grid_size, max_word_len) in enumerate(difficulties):
            rect = pygame.Rect(screen.get_width()//2 - 100, 150 + i*80, 200, 50)
            diff_rects.append((rect, grid_size, max_word_len))
            pygame.draw.rect(screen, (70, 130, 180), rect)
            text = small_font.render(label, True, (255, 255, 255))
            screen.blit(text, (rect.x + 60, rect.y + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, grid_size, max_word_len in diff_rects:
                    if rect.collidepoint(pos):
                        selected_diff = (grid_size, max_word_len)

    return (*selected_diff, selected_mode)
